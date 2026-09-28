#!/usr/bin/env python3
"""Inventaria e baixa PDFs de um pacote matriculado no Estratégia.

O navegador autenticado continua sendo a fonte de autorização. O script visita
somente páginas normais do pacote, curso e aula, e baixa os links de livros
eletrônicos que a própria interface apresenta. Links de slides/vídeos não entram
neste fluxo.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
import unicodedata
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from estrategia_cdp import CDP, active_page, wait_until_loaded


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = "https://www.estrategiaconcursos.com.br"
API_HOST = "api.estrategiaconcursos.com.br"


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def slug(text: str, limit: int = 80) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode().lower()
    value = re.sub(r"[^a-z0-9]+", "-", ascii_text).strip("-")
    return (value[:limit].rstrip("-") or "material")


def wait_for(cdp: CDP, expression: str, label: str, timeout: float = 30) -> None:
    deadline = time.monotonic() + timeout
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        try:
            if cdp.evaluate(expression):
                return
        except (ConnectionError, RuntimeError) as error:
            last_error = error
        time.sleep(0.25)
    suffix = f": {last_error}" if last_error else ""
    raise TimeoutError(f"Timeout ao aguardar {label}{suffix}")


def navigate(cdp: CDP, url: str, ready_expression: str, label: str) -> None:
    cdp.call("Page.navigate", {"url": url})
    wait_until_loaded(cdp)
    wait_for(cdp, ready_expression, label)


def read_package(cdp: CDP, package_id: str) -> dict:
    url = f"{SITE_ROOT}/app/dashboard/pacote/{package_id}"
    api_fragment = f"/api/aluno/pacote/{package_id}"
    navigate(
        cdp,
        url,
        f"performance.getEntriesByType('resource').some(e => e.name.includes('{api_fragment}'))",
        "detalhes do pacote",
    )
    result = cdp.evaluate(
        r"""
        (() => {
          const pageTitle = [...document.querySelectorAll('h1,h2,h3')]
            .map(e => e.innerText.trim())
            .find(text => text.includes('Pacote Teórico'));
          const seen = new Set();
          const courses = [];
          for (const anchor of document.querySelectorAll(
            'a[href*="/app/dashboard/cursos/"][href*="/aulas"]'
          )) {
            const match = new URL(anchor.href).pathname.match(
              /^\/app\/dashboard\/cursos\/(\d+)\/aulas\/?$/
            );
            if (!match || seen.has(match[1])) continue;
            seen.add(match[1]);
            courses.push({
              id: match[1],
              name: anchor.innerText.trim(),
              url: anchor.href
            });
          }
          return {
            name: pageTitle || document.title,
            url: location.href,
            authenticated: Boolean(document.querySelector('a[href*="/logout"]')),
            courses
          };
        })()
        """
    )
    if not result["authenticated"]:
        raise RuntimeError("A sessão não está autenticada")
    if not result["courses"]:
        raise RuntimeError("Nenhum curso componente foi encontrado no pacote")
    return {"id": package_id, **result}


def read_course_lessons(cdp: CDP, course: dict) -> dict:
    api_fragment = f"/api/aluno/curso/{course['id']}"
    navigate(
        cdp,
        course["url"],
        f"performance.getEntriesByType('resource').some(e => e.name.includes('{api_fragment}'))",
        f"curso {course['id']}",
    )
    time.sleep(0.4)
    result = cdp.evaluate(
        r"""
        (() => {
          const seen = new Set();
          const lessons = [];
          for (const anchor of document.querySelectorAll('a.Collapse-header[href]')) {
            const match = new URL(anchor.href).pathname.match(
              /^\/app\/dashboard\/cursos\/(\d+)\/aulas\/(\d+)/
            );
            if (!match || seen.has(match[2])) continue;
            seen.add(match[2]);
            const lines = anchor.innerText.split('\n')
              .map(line => line.trim()).filter(Boolean);
            lessons.push({
              id: match[2],
              label: lines[0] || `Aula ${lessons.length}`,
              title: lines.slice(1).join(' - '),
              url: `${location.origin}/app/dashboard/cursos/${match[1]}/aulas/${match[2]}`
            });
          }
          const names = [...document.querySelectorAll('h1,h2,h3')]
            .map(e => e.innerText.trim()).filter(Boolean);
          return {name: names.find(name => name !== 'Curso' && !/^Aula /i.test(name)), lessons};
        })()
        """
    )
    return {
        **course,
        "name": result.get("name") or course["name"],
        "lesson_count": len(result["lessons"]),
        "lessons": result["lessons"],
    }


def inventory_package(cdp: CDP, package_id: str, output: Path) -> dict:
    package = read_package(cdp, package_id)
    inventory = {
        "schema_version": 1,
        "collected_at": now_iso(),
        "package": package,
        "course_count": len(package["courses"]),
        "lesson_count": 0,
        "courses": [],
    }
    print(
        json.dumps(
            {"package_id": package_id, "courses": len(package["courses"])},
            ensure_ascii=False,
        ),
        flush=True,
    )
    for index, course in enumerate(package["courses"], start=1):
        detailed = read_course_lessons(cdp, course)
        inventory["courses"].append(detailed)
        inventory["lesson_count"] += detailed["lesson_count"]
        write_json(output, inventory)
        print(
            json.dumps(
                {
                    "course": index,
                    "total_courses": len(package["courses"]),
                    "id": detailed["id"],
                    "lessons": detailed["lesson_count"],
                    "name": detailed["name"],
                },
                ensure_ascii=False,
            ),
            flush=True,
        )
    inventory["completed_at"] = now_iso()
    write_json(output, inventory)
    return inventory


def read_lesson_pdfs(cdp: CDP, course: dict, lesson: dict) -> list[dict]:
    api_fragment = f"/api/aluno/aula/{lesson['id']}"
    navigate(
        cdp,
        lesson["url"],
        f"performance.getEntriesByType('resource').some(e => e.name.includes('{api_fragment}'))",
        f"aula {lesson['id']}",
    )
    time.sleep(0.35)
    links = cdp.evaluate(
        r"""
        (() => [...document.querySelectorAll('a.LessonButton[href]')]
          .filter(anchor => {
            const url = new URL(anchor.href);
            return url.hostname === 'api.estrategiaconcursos.com.br' &&
              url.pathname.includes('/api/aluno/pdf/');
          })
          .map(anchor => ({
            title: anchor.innerText.trim().replace(/\s+/g, ' ')
              .replace(/\s+Baixado$/i, ''),
            download_url: anchor.href
          })))()
        """
    )
    unique = {}
    for item in links:
        unique[item["title"]] = item
    return list(unique.values())


def download_pdf(url: str, destination: Path, referer: str) -> tuple[int, str]:
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != API_HOST:
        raise RuntimeError(f"Origem de download não autorizada: {parsed.hostname}")
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": referer,
            "Accept": "application/pdf,application/octet-stream;q=0.9,*/*;q=0.8",
        },
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".part")
    digest = hashlib.sha256()
    size = 0
    try:
        with urllib.request.urlopen(request, timeout=120) as response, temporary.open("wb") as target:
            first = response.read(8192)
            if not first.startswith(b"%PDF"):
                raise RuntimeError(
                    f"Resposta não é PDF (HTTP {response.status}, "
                    f"Content-Type {response.headers.get('Content-Type')})"
                )
            target.write(first)
            digest.update(first)
            size += len(first)
            while chunk := response.read(1024 * 1024):
                target.write(chunk)
                digest.update(chunk)
                size += len(chunk)
        temporary.replace(destination)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise
    return size, digest.hexdigest()


def download_pdf_with_retries(
    url: str, destination: Path, referer: str, attempts: int = 3
) -> tuple[int, str]:
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            return download_pdf(url, destination, referer)
        except (OSError, urllib.error.URLError, RuntimeError) as error:
            last_error = error
            if attempt < attempts:
                time.sleep(attempt)
    assert last_error is not None
    raise last_error


def material_key(course_id: str, lesson_id: str, title: str) -> str:
    return f"{course_id}:{lesson_id}:{title}"


def download_inventory(
    cdp: CDP,
    inventory: dict,
    manifest_path: Path,
    download_root: Path,
    limit: int | None = None,
    lesson_ids: set[str] | None = None,
) -> dict:
    download_root = download_root.resolve()
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    else:
        manifest = {
            "schema_version": 1,
            "package_id": inventory["package"]["id"],
            "curso": inventory["package"]["name"],
            "url_origem": inventory["package"]["url"],
            "iniciado_em": now_iso(),
            "materiais": [],
            "erros": [],
        }
    completed = {
        material_key(item["curso_id"], item["aula_id"], item["titulo"]): item
        for item in manifest["materiais"]
        if item.get("baixado_em")
    }
    processed = 0
    for course_index, course in enumerate(inventory["courses"], start=1):
        course_dir = download_root / f"{course_index:02d}-{slug(course['name'], 90)}"
        for lesson_index, lesson in enumerate(course["lessons"], start=1):
            if lesson_ids and lesson["id"] not in lesson_ids:
                continue
            pdfs = read_lesson_pdfs(cdp, course, lesson)
            if not pdfs:
                print(
                    json.dumps(
                        {
                            "course_id": course["id"],
                            "lesson_id": lesson["id"],
                            "pdfs": 0,
                        }
                    ),
                    flush=True,
                )
                continue
            for variant_index, pdf in enumerate(pdfs, start=1):
                key = material_key(course["id"], lesson["id"], pdf["title"])
                if key in completed:
                    path = PROJECT_ROOT / completed[key]["arquivo"]
                    if path.is_file() and path.stat().st_size == completed[key]["tamanho_bytes"]:
                        print(json.dumps({"skipped": key}), flush=True)
                        continue
                filename = (
                    f"{lesson_index:03d}-{slug(lesson['label'], 30)}-"
                    f"{lesson['id']}-{variant_index:02d}-{slug(pdf['title'], 50)}.pdf"
                )
                destination = course_dir / filename
                try:
                    size, sha256 = download_pdf_with_retries(
                        pdf["download_url"], destination, lesson["url"]
                    )
                except (OSError, urllib.error.URLError, RuntimeError) as error:
                    failure = {
                        "curso_id": course["id"],
                        "aula_id": lesson["id"],
                        "titulo": pdf["title"],
                        "erro": str(error),
                        "ocorrido_em": now_iso(),
                    }
                    manifest["erros"].append(failure)
                    write_json(manifest_path, manifest)
                    print(json.dumps(failure, ensure_ascii=False), flush=True)
                    continue
                record = {
                    "disciplina": course["name"],
                    "curso_id": course["id"],
                    "aula": lesson["label"],
                    "aula_id": lesson["id"],
                    "titulo_aula": lesson["title"],
                    "titulo": pdf["title"],
                    "arquivo": str(destination.relative_to(PROJECT_ROOT)),
                    "url_origem": lesson["url"],
                    "baixado_em": now_iso(),
                    "tamanho_bytes": size,
                    "sha256": sha256,
                }
                previous = next(
                    (
                        index
                        for index, item in enumerate(manifest["materiais"])
                        if material_key(
                            item["curso_id"], item["aula_id"], item["titulo"]
                        )
                        == key
                    ),
                    None,
                )
                if previous is None:
                    manifest["materiais"].append(record)
                else:
                    manifest["materiais"][previous] = record
                completed[key] = record
                manifest["erros"] = [
                    error
                    for error in manifest["erros"]
                    if not (
                        error.get("curso_id") == course["id"]
                        and error.get("aula_id") == lesson["id"]
                        and error.get("titulo") == pdf["title"]
                    )
                ]
                manifest["atualizado_em"] = now_iso()
                write_json(manifest_path, manifest)
                processed += 1
                print(
                    json.dumps(
                        {
                            "downloaded": str(destination.relative_to(PROJECT_ROOT)),
                            "bytes": size,
                            "progress_this_run": processed,
                        },
                        ensure_ascii=False,
                    ),
                    flush=True,
                )
                if limit is not None and processed >= limit:
                    return manifest
    manifest["concluido_em"] = now_iso()
    manifest["total_materiais"] = len(manifest["materiais"])
    write_json(manifest_path, manifest)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inventário e download retomável dos PDFs de um pacote"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    inventory = subparsers.add_parser("inventory")
    inventory.add_argument("package_id")
    inventory.add_argument("--output", type=Path, required=True)

    download = subparsers.add_parser("download")
    download.add_argument("inventory", type=Path)
    download.add_argument("--manifest", type=Path, required=True)
    download.add_argument("--download-dir", type=Path, required=True)
    download.add_argument("--limit", type=int)
    download.add_argument(
        "--lesson-id",
        action="append",
        help="restringe a uma aula; pode ser repetido",
    )
    args = parser.parse_args()

    cdp = CDP(active_page())
    try:
        if args.command == "inventory":
            result = inventory_package(cdp, args.package_id, args.output)
            summary = {
                "package_id": args.package_id,
                "courses": result["course_count"],
                "lessons": result["lesson_count"],
                "output": str(args.output),
            }
        else:
            source = json.loads(args.inventory.read_text(encoding="utf-8"))
            result = download_inventory(
                cdp,
                source,
                args.manifest,
                args.download_dir,
                args.limit,
                set(args.lesson_id) if args.lesson_id else None,
            )
            summary = {
                "downloaded": len(result["materiais"]),
                "errors": len(result["erros"]),
                "manifest": str(args.manifest),
            }
    finally:
        cdp.close()
    print(json.dumps(summary, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
