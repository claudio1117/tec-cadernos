#!/usr/bin/env python3
"""Cliente CDP mínimo para investigar a página autenticada do Estratégia.

Usa somente a biblioteca padrão e se conecta ao Chrome iniciado por
``estrategia_browser.py``. Este módulo não contém seletores da plataforma nem
executa downloads.
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
from pathlib import Path
from urllib.parse import urlparse


DEBUG_URL = os.environ.get(
    "ESTRATEGIA_DEBUG_URL", "http://127.0.0.1:9223"
).rstrip("/")
TARGET_PREFIX = "https://www.estrategiaconcursos.com.br/"


def list_pages() -> list[dict]:
    with urllib.request.urlopen(f"{DEBUG_URL}/json/list", timeout=5) as response:
        return json.load(response)


def active_page() -> dict:
    pages = [page for page in list_pages() if page.get("type") == "page"]
    if not pages:
        raise RuntimeError("Nenhuma página comum encontrada no Chrome")
    return next(
        (page for page in pages if page.get("url", "").startswith(TARGET_PREFIX)),
        pages[0],
    )


class WebSocket:
    """Implementação estritamente necessária para mensagens de texto do CDP."""

    def __init__(self, url: str):
        parsed = urlparse(url)
        self.sock = socket.create_connection((parsed.hostname, parsed.port), timeout=10)
        self.sock.settimeout(60)
        key = base64.b64encode(os.urandom(16)).decode()
        path = parsed.path + (f"?{parsed.query}" if parsed.query else "")
        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {parsed.hostname}:{parsed.port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n"
            f"Origin: {DEBUG_URL}\r\n\r\n"
        )
        self.sock.sendall(request.encode())
        response = self._read_headers()
        if " 101 " not in response.split("\r\n", 1)[0]:
            raise RuntimeError(f"Falha no WebSocket: {response.splitlines()[0]}")
        expected = base64.b64encode(
            hashlib.sha1(
                (key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode()
            ).digest()
        ).decode()
        if f"Sec-WebSocket-Accept: {expected}".lower() not in response.lower():
            raise RuntimeError("Resposta WebSocket inválida")

    def _read_headers(self) -> str:
        data = bytearray()
        while b"\r\n\r\n" not in data:
            chunk = self.sock.recv(1)
            if not chunk:
                raise ConnectionError("WebSocket encerrado durante a conexão")
            data.extend(chunk)
        return data.decode(errors="replace")

    def _read_exact(self, size: int) -> bytes:
        data = bytearray()
        while len(data) < size:
            chunk = self.sock.recv(size - len(data))
            if not chunk:
                raise ConnectionError("WebSocket encerrado")
            data.extend(chunk)
        return bytes(data)

    def _send_control(self, opcode: int, payload: bytes) -> None:
        mask = os.urandom(4)
        masked = bytes(byte ^ mask[index % 4] for index, byte in enumerate(payload))
        self.sock.sendall(
            bytes([0x80 | opcode, 0x80 | len(payload)]) + mask + masked
        )

    def send_text(self, text: str) -> None:
        payload = text.encode()
        size = len(payload)
        header = bytearray([0x81])
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
            mask = self._read_exact(4) if second & 0x80 else b""
            payload = self._read_exact(size)
            if mask:
                payload = bytes(
                    byte ^ mask[index % 4] for index, byte in enumerate(payload)
                )
            if opcode == 0x8:
                raise ConnectionError("WebSocket encerrado pelo Chrome")
            if opcode == 0x9:
                self._send_control(0xA, payload)
                continue
            if opcode in (0x0, 0x1):
                fragments.extend(payload)
                if final:
                    return fragments.decode()

    def close(self) -> None:
        self.sock.close()


class CDP:
    def __init__(self, page: dict):
        self.websocket = WebSocket(page["webSocketDebuggerUrl"])
        self.sequence = 0

    def call(self, method: str, params: dict | None = None) -> dict:
        self.sequence += 1
        call_id = self.sequence
        self.websocket.send_text(
            json.dumps({"id": call_id, "method": method, "params": params or {}})
        )
        while True:
            response = json.loads(self.websocket.receive_text())
            if response.get("id") == call_id:
                if "error" in response:
                    raise RuntimeError(response["error"])
                return response.get("result", {})

    def evaluate(self, expression: str):
        response = self.call(
            "Runtime.evaluate",
            {
                "expression": expression,
                "returnByValue": True,
                "awaitPromise": True,
            },
        )
        if response.get("exceptionDetails"):
            details = response["exceptionDetails"]
            exception = details.get("exception", {})
            raise RuntimeError(exception.get("description") or details.get("text"))
        result = response.get("result", {})
        if result.get("subtype") == "error":
            raise RuntimeError(result.get("description", "Erro JavaScript"))
        return result.get("value")

    def close(self) -> None:
        self.websocket.close()


def wait_until_loaded(cdp: CDP, timeout: float = 30) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if cdp.evaluate("document.readyState") == "complete":
            return
        time.sleep(0.25)
    raise TimeoutError("A página não terminou de carregar")


def page_state(cdp: CDP):
    return cdp.evaluate(
        """
        (() => ({
          title: document.title,
          url: location.href,
          readyState: document.readyState,
          headings: [...document.querySelectorAll('h1,h2,h3')]
            .map(element => element.innerText.trim()).filter(Boolean),
          links: [...document.querySelectorAll('a[href]')]
            .map(element => ({
              text: element.innerText.trim(),
              href: element.href,
              className: element.className
            }))
            .filter(item => item.text)
        }))()
        """
    )


def enrolled_courses(cdp: CDP):
    """Extrai cartões de matrícula visíveis, sem navegar ou alterar a página."""
    return cdp.evaluate(
        """
        (() => {
          const groups = [];
          const courses = [];
          const otherEntitlements = [];
          let section = null;
          const nodes = document.querySelectorAll(
            'h2.SectionTitle, a[href]'
          );
          for (const node of nodes) {
            if (node.matches('h2.SectionTitle')) {
              section = node.innerText.trim();
              continue;
            }
            const heading = node.querySelector('h1');
            const text = node.innerText.trim();
            const availability = text.match(
              /Disponível entre\\s+(\\d{2}\\/\\d{2}\\/\\d{4})\\s+e\\s+(\\d{2}\\/\\d{2}\\/\\d{4})/
            );
            if (!heading || !availability) continue;
            const route = new URL(node.href).pathname.match(
              /^\\/app\\/dashboard\\/cursos\\/(\\d+)\\/aulas\\/?$/
            );
            const item = {
              section,
              name: heading.innerText.trim(),
              url: node.href,
              available_from: availability[1],
              available_until: availability[2]
            };
            if (route) courses.push({...item, id: route[1]});
            else otherEntitlements.push(item);
          }
          for (const course of courses) {
            let group = groups.find(item => item.name === course.section);
            if (!group) {
              group = {name: course.section, courses: []};
              groups.push(group);
            }
            const {section: ignored, ...normalized} = course;
            group.courses.push(normalized);
          }
          return {
            collected_at: new Date().toISOString(),
            source_url: location.href,
            authenticated: Boolean(document.querySelector('a[href*="/logout"]')),
            course_count: courses.length,
            groups,
            other_entitlements: otherEntitlements
          };
        })()
        """
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspeção local via CDP")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("state", help="resume a página autenticada")
    subparsers.add_parser("courses", help="lista os cartões de cursos matriculados")
    navigate = subparsers.add_parser("navigate", help="abre uma URL na aba autenticada")
    navigate.add_argument("url")
    evaluate = subparsers.add_parser("eval", help="avalia JavaScript na aba")
    evaluate.add_argument("expression")
    parser.add_argument("--output", type=Path, help="salva o resultado em JSON")
    args = parser.parse_args()

    cdp = CDP(active_page())
    try:
        if args.command == "state":
            output = page_state(cdp)
        elif args.command == "courses":
            output = enrolled_courses(cdp)
        elif args.command == "navigate":
            cdp.call("Page.navigate", {"url": args.url})
            wait_until_loaded(cdp)
            output = cdp.evaluate("({title: document.title, url: location.href})")
        else:
            output = cdp.evaluate(args.expression)
    finally:
        cdp.close()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(output, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    json.dump(output, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
