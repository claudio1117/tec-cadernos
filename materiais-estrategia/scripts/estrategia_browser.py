#!/usr/bin/env python3
"""Inicia e diagnostica o Chrome dedicado à automação do Estratégia.

Este módulo não acessa a conta nem automatiza downloads. Ele apenas inicia um
Chrome com perfil persistente e depuração remota local, deixando a sessão pronta
para a inspeção via Chrome DevTools Protocol (CDP) em uma etapa posterior.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROFILE_DIR = PROJECT_ROOT / ".chrome-estrategia-profile"
DEFAULT_START_URL = "https://www.estrategiaconcursos.com.br/"
DEFAULT_DEBUG_HOST = "127.0.0.1"
DEFAULT_DEBUG_PORT = 9223
BROWSER_CANDIDATES = (
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
)


def find_browser(explicit: str | None = None) -> str:
    """Localiza Chrome/Chromium, respeitando a escolha explícita do usuário."""
    requested = explicit or os.environ.get("ESTRATEGIA_CHROME_BINARY")
    if requested:
        resolved = shutil.which(requested)
        candidate = Path(requested).expanduser()
        if resolved:
            return resolved
        if candidate.is_file():
            return str(candidate.resolve())
        raise FileNotFoundError(f"Navegador não encontrado: {requested}")

    for name in BROWSER_CANDIDATES:
        resolved = shutil.which(name)
        if resolved:
            return resolved
    raise FileNotFoundError(
        "Chrome/Chromium não encontrado. Informe --browser ou "
        "ESTRATEGIA_CHROME_BINARY."
    )


def debug_url(host: str, port: int) -> str:
    return f"http://{host}:{port}"


def read_json(url: str, timeout: float = 2.0):
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return json.load(response)


def read_status(host: str, port: int) -> dict:
    """Lê somente os endpoints HTTP de descoberta do CDP."""
    base_url = debug_url(host, port)
    version = read_json(f"{base_url}/json/version")
    targets = read_json(f"{base_url}/json/list")
    pages = [
        {
            "id": target.get("id"),
            "title": target.get("title"),
            "url": target.get("url"),
        }
        for target in targets
        if target.get("type") == "page"
    ]
    return {
        "connected": True,
        "debug_url": base_url,
        "browser": version.get("Browser"),
        "protocol_version": version.get("Protocol-Version"),
        "pages": pages,
    }


def build_command(
    browser: str,
    profile_dir: Path,
    host: str,
    port: int,
    start_url: str,
) -> list[str]:
    origin = debug_url(host, port)
    return [
        browser,
        f"--remote-debugging-address={host}",
        f"--remote-debugging-port={port}",
        f"--remote-allow-origins={origin}",
        f"--user-data-dir={profile_dir}",
        "--no-first-run",
        "--no-default-browser-check",
        start_url,
    ]


def wait_for_cdp(host: str, port: int, timeout: float) -> dict:
    deadline = time.monotonic() + timeout
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        try:
            return read_status(host, port)
        except (OSError, urllib.error.URLError, json.JSONDecodeError) as error:
            last_error = error
            time.sleep(0.25)
    raise TimeoutError(
        f"O endpoint CDP não respondeu em {debug_url(host, port)} após "
        f"{timeout:g}s: {last_error}"
    )


def print_json(value: dict) -> None:
    json.dump(value, sys.stdout, ensure_ascii=False, indent=2)
    print()
    sys.stdout.flush()


def start_browser(args: argparse.Namespace) -> None:
    try:
        current = read_status(args.host, args.port)
    except (OSError, urllib.error.URLError, json.JSONDecodeError):
        current = None
    if current:
        current["started"] = False
        current["reason"] = "Já existe um navegador expondo esta porta CDP."
        print_json(current)
        return

    browser = find_browser(args.browser)
    profile_dir = args.profile_dir.expanduser().resolve()
    command = build_command(browser, profile_dir, args.host, args.port, args.url)
    if args.dry_run:
        print_json(
            {
                "dry_run": True,
                "profile_dir": str(profile_dir),
                "command": command,
            }
        )
        return

    profile_dir.mkdir(parents=True, exist_ok=True)
    process = subprocess.Popen(
        command,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    try:
        status = wait_for_cdp(args.host, args.port, args.timeout)
    except Exception:
        if process.poll() is None:
            process.terminate()
        raise
    status.update(
        {
            "started": True,
            "pid": process.pid,
            "profile_dir": str(profile_dir),
        }
    )
    print_json(status)
    if args.wait:
        try:
            process.wait()
        except KeyboardInterrupt:
            process.terminate()


def show_status(args: argparse.Namespace) -> None:
    try:
        print_json(read_status(args.host, args.port))
    except (OSError, urllib.error.URLError, json.JSONDecodeError) as error:
        raise RuntimeError(
            f"Chrome indisponível em {debug_url(args.host, args.port)}. "
            "Execute primeiro o comando start."
        ) from error


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Chrome dedicado e endpoint CDP do Estratégia Concursos"
    )
    parser.add_argument(
        "--host",
        default=os.environ.get("ESTRATEGIA_DEBUG_HOST", DEFAULT_DEBUG_HOST),
        help="endereço local do CDP (padrão: %(default)s)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("ESTRATEGIA_DEBUG_PORT", DEFAULT_DEBUG_PORT)),
        help="porta do CDP (padrão: %(default)s)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    start = subparsers.add_parser("start", help="inicia o perfil dedicado")
    start.add_argument("--browser", help="executável do Chrome/Chromium")
    start.add_argument(
        "--profile-dir",
        type=Path,
        default=DEFAULT_PROFILE_DIR,
        help="diretório persistente do perfil",
    )
    start.add_argument(
        "--url",
        default=os.environ.get("ESTRATEGIA_START_URL", DEFAULT_START_URL),
        help="URL inicial",
    )
    start.add_argument("--timeout", type=float, default=15.0)
    start.add_argument(
        "--dry-run",
        action="store_true",
        help="mostra o comando sem iniciar o navegador",
    )
    start.add_argument(
        "--wait",
        action="store_true",
        help="mantém o launcher ativo até a janela do Chrome ser fechada",
    )
    start.set_defaults(handler=start_browser)

    status = subparsers.add_parser("status", help="confere o endpoint CDP")
    status.set_defaults(handler=show_status)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.host not in {"127.0.0.1", "localhost", "::1"}:
        parser.error("por segurança, o endpoint CDP deve permanecer no host local")
    if not 1 <= args.port <= 65535:
        parser.error("a porta deve estar entre 1 e 65535")
    try:
        args.handler(args)
    except (FileNotFoundError, RuntimeError, TimeoutError) as error:
        parser.exit(1, f"erro: {error}\n")


if __name__ == "__main__":
    main()
