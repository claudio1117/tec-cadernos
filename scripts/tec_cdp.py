#!/usr/bin/env python3
"""Cliente mínimo do Chrome DevTools Protocol para a automação do TEC.

Usa apenas a biblioteca padrão. O Chrome deve ser iniciado com
--remote-debugging-port=9222 e --remote-allow-origins=*.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import socket
import struct
import sys
import time
import urllib.request
from urllib.parse import urlparse


DEBUG_URL = "http://127.0.0.1:9222"


def list_pages() -> list[dict]:
    with urllib.request.urlopen(f"{DEBUG_URL}/json", timeout=5) as response:
        return json.load(response)


def active_page() -> dict:
    pages = [page for page in list_pages() if page.get("type") == "page"]
    if not pages:
        raise RuntimeError("Nenhuma página comum encontrada no Chrome")
    return pages[0]


class WebSocket:
    def __init__(self, url: str):
        parsed = urlparse(url)
        self.sock = socket.create_connection((parsed.hostname, parsed.port), timeout=10)
        self.sock.settimeout(60)
        key = base64.b64encode(os.urandom(16)).decode()
        request = (
            f"GET {parsed.path} HTTP/1.1\r\n"
            f"Host: {parsed.hostname}:{parsed.port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n"
            "Origin: http://127.0.0.1:9222\r\n\r\n"
        )
        self.sock.sendall(request.encode())
        response = self._read_headers()
        if " 101 " not in response.split("\r\n", 1)[0]:
            raise RuntimeError(f"Falha no WebSocket: {response.splitlines()[0]}")
        expected = base64.b64encode(
            hashlib.sha1((key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode()).digest()
        ).decode()
        if f"Sec-WebSocket-Accept: {expected}".lower() not in response.lower():
            raise RuntimeError("Resposta WebSocket inválida")

    def _read_headers(self) -> str:
        data = bytearray()
        while b"\r\n\r\n" not in data:
            data.extend(self.sock.recv(4096))
        return data.decode(errors="replace")

    def _read_exact(self, size: int) -> bytes:
        data = bytearray()
        while len(data) < size:
            chunk = self.sock.recv(size - len(data))
            if not chunk:
                raise ConnectionError("WebSocket encerrado")
            data.extend(chunk)
        return bytes(data)

    def send_text(self, text: str) -> None:
        payload = text.encode()
        header = bytearray([0x81])
        size = len(payload)
        if size < 126:
            header.append(0x80 | size)
        elif size < 65536:
            header.append(0x80 | 126)
            header.extend(struct.pack("!H", size))
        else:
            header.append(0x80 | 127)
            header.extend(struct.pack("!Q", size))
        mask = os.urandom(4)
        masked = bytes(byte ^ mask[index % 4] for index, byte in enumerate(payload))
        self.sock.sendall(bytes(header) + mask + masked)

    def receive_text(self) -> str:
        fragments = bytearray()
        while True:
            first, second = self._read_exact(2)
            final = bool(first & 0x80)
            opcode = first & 0x0F
            size = second & 0x7F
            if size == 126:
                size = struct.unpack("!H", self._read_exact(2))[0]
            elif size == 127:
                size = struct.unpack("!Q", self._read_exact(8))[0]
            masked = bool(second & 0x80)
            mask = self._read_exact(4) if masked else b""
            payload = self._read_exact(size)
            if masked:
                payload = bytes(byte ^ mask[index % 4] for index, byte in enumerate(payload))
            if opcode == 0x8:
                raise ConnectionError("WebSocket encerrado pelo Chrome")
            if opcode == 0x9:
                self._send_control(0xA, payload)
                continue
            if opcode in (0x0, 0x1):
                fragments.extend(payload)
                if final:
                    return fragments.decode()

    def _send_control(self, opcode: int, payload: bytes) -> None:
        mask = os.urandom(4)
        masked = bytes(byte ^ mask[index % 4] for index, byte in enumerate(payload))
        self.sock.sendall(bytes([0x80 | opcode, 0x80 | len(payload)]) + mask + masked)


class CDP:
    def __init__(self, page: dict):
        self.ws = WebSocket(page["webSocketDebuggerUrl"])
        self.sequence = 0

    def call(self, method: str, params: dict | None = None) -> dict:
        self.sequence += 1
        call_id = self.sequence
        message = {"id": call_id, "method": method, "params": params or {}}
        self.ws.send_text(json.dumps(message))
        while True:
            response = json.loads(self.ws.receive_text())
            if response.get("id") == call_id:
                if "error" in response:
                    raise RuntimeError(response["error"])
                return response.get("result", {})

    def evaluate(self, expression: str):
        result = self.call(
            "Runtime.evaluate",
            {"expression": expression, "returnByValue": True, "awaitPromise": True},
        )
        value = result.get("result", {})
        if value.get("subtype") == "promise" and value.get("objectId"):
            awaited = self.call(
                "Runtime.awaitPromise",
                {"promiseObjectId": value["objectId"], "returnByValue": True},
            )
            value = awaited.get("result", {})
        if value.get("subtype") == "error":
            raise RuntimeError(value.get("description", "Erro JavaScript"))
        return value.get("value")

    def evaluate_async(self, expression: str):
        initial = self.call(
            "Runtime.evaluate",
            {"expression": expression, "returnByValue": False, "awaitPromise": False},
        ).get("result", {})
        if initial.get("subtype") != "promise" or not initial.get("objectId"):
            raise RuntimeError("A expressão assíncrona não retornou uma Promise")
        awaited_response = self.call(
            "Runtime.awaitPromise",
            {"promiseObjectId": initial["objectId"], "returnByValue": True},
        )
        if awaited_response.get("exceptionDetails"):
            details = awaited_response["exceptionDetails"]
            description = details.get("exception", {}).get("description") or details.get("text")
            raise RuntimeError(description or "Erro JavaScript assíncrono")
        awaited = awaited_response.get("result", {})
        if awaited.get("subtype") == "error":
            raise RuntimeError(awaited.get("description", "Erro JavaScript assíncrono"))
        return awaited.get("value")


def wait_until_loaded(cdp: CDP, timeout: int = 30) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if cdp.evaluate("document.readyState") == "complete":
            return
        time.sleep(0.25)
    raise TimeoutError("A página não terminou de carregar")


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("state")
    navigate = subparsers.add_parser("navigate")
    navigate.add_argument("url")
    evaluate = subparsers.add_parser("eval")
    evaluate.add_argument("expression")
    evaluate64 = subparsers.add_parser("eval64")
    evaluate64.add_argument("expression_base64")
    evaluate_hex = subparsers.add_parser("evalhex")
    evaluate_hex.add_argument("expression_hex")
    evaluate_async_hex = subparsers.add_parser("evalasynchex")
    evaluate_async_hex.add_argument("expression_hex")
    args = parser.parse_args()

    page = active_page()
    cdp = CDP(page)
    if args.command == "state":
        output = cdp.evaluate(
            "({title: document.title, url: location.href, "
            "headings: [...document.querySelectorAll('h1,h2,h3')].map(e => e.innerText.trim()).filter(Boolean), "
            "buttons: [...document.querySelectorAll('button,a.btn')].map(e => ({text:e.innerText.trim(),id:e.id,cls:e.className})).filter(e => e.text), "
            "inputs: [...document.querySelectorAll('input,select,textarea')].map(e => ({tag:e.tagName,type:e.type,id:e.id,name:e.name,placeholder:e.placeholder}))})"
        )
    elif args.command == "navigate":
        cdp.call("Page.navigate", {"url": args.url})
        wait_until_loaded(cdp)
        output = cdp.evaluate("({title: document.title, url: location.href})")
    elif args.command == "eval":
        output = cdp.evaluate(args.expression)
    elif args.command == "eval64":
        expression = base64.b64decode(args.expression_base64).decode()
        output = cdp.evaluate(expression)
    elif args.command == "evalhex":
        expression = bytes.fromhex(args.expression_hex).decode()
        output = cdp.evaluate(expression)
    else:
        expression = bytes.fromhex(args.expression_hex).decode()
        output = cdp.evaluate_async(expression)
    json.dump(output, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
