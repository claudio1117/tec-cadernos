from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import unicodedata
import uuid
from collections import OrderedDict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
CHUNK_SIZE = 1024 * 1024


class ProcessingError(RuntimeError):
    """Erro que impede o início do processamento."""


@dataclass(frozen=True)
class ProcessingResult:
    manifest_path: Path
    index_path: Path
    report_path: Path
    summary: dict[str, int]


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def slugify(value: str, max_length: int = 90) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_value).strip("-").lower()
    return (slug[:max_length].rstrip("-") or "sem-nome")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _portable_path(path: Path, project_root: Path) -> str:
    absolute = path.resolve()
    try:
        return absolute.relative_to(project_root.resolve()).as_posix()
    except ValueError:
        return absolute.as_posix()


def _resolve_project_path(value: str, project_root: Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = project_root / path
    return path.resolve()


def _read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ProcessingError(f"arquivo não encontrado: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ProcessingError(f"JSON inválido em {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ProcessingError(f"o JSON deve conter um objeto na raiz: {path}")
    return data


def _write_json_atomic(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    try:
        temporary.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _discover_manifest(project_root: Path, requested: Path | None) -> Path:
    if requested:
        path = requested if requested.is_absolute() else project_root / requested
        if not path.is_file():
            raise ProcessingError(f"manifesto-fonte não encontrado: {path}")
        return path.resolve()

    candidates: list[Path] = []
    for path in sorted((project_root / "data" / "manifests").glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(data, dict) and isinstance(data.get("materiais"), list):
            candidates.append(path)

    if not candidates:
        raise ProcessingError("nenhum manifesto bruto encontrado em data/manifests")
    if len(candidates) > 1:
        names = ", ".join(path.name for path in candidates)
        raise ProcessingError(
            "há mais de um manifesto; use --manifesto-fonte. Encontrados: " + names
        )
    return candidates[0].resolve()


def _validate_source(data: dict[str, Any], path: Path) -> list[str]:
    failures: list[str] = []
    if not isinstance(data.get("curso"), str) or not data["curso"].strip():
        failures.append("campo de topo 'curso' ausente ou inválido")
    materials = data.get("materiais")
    if not isinstance(materials, list):
        failures.append("campo de topo 'materiais' deve ser uma lista")
    elif not materials:
        failures.append("o manifesto não contém materiais")
    else:
        required = ("disciplina", "aula", "titulo", "arquivo", "baixado_em")
        for index, material in enumerate(materials, 1):
            if not isinstance(material, dict):
                failures.append(f"material {index}: registro não é um objeto")
                continue
            missing = [field for field in required if not material.get(field)]
            if missing:
                failures.append(
                    f"material {index}: campos obrigatórios ausentes: {', '.join(missing)}"
                )
    if failures:
        preview = "; ".join(failures[:10])
        suffix = " ..." if len(failures) > 10 else ""
        raise ProcessingError(f"manifesto-fonte inválido ({path}): {preview}{suffix}")
    return failures


def _material_id(material: dict[str, Any]) -> str:
    stable_parts = (
        str(material.get("curso_id", "")),
        str(material.get("aula_id", "")),
        str(material.get("titulo", "")),
        str(material.get("arquivo", "")),
    )
    suffix = hashlib.sha256("\0".join(stable_parts).encode("utf-8")).hexdigest()[:12]
    aula_id = slugify(str(material.get("aula_id") or material.get("aula") or "aula"), 32)
    return f"{aula_id}-{suffix}"


def _text_path(
    material: dict[str, Any],
    material_id: str,
    texts_root: Path,
    course_slug: str,
) -> Path:
    discipline_id = str(material.get("curso_id") or "disciplina")
    discipline = f"{slugify(discipline_id, 24)}-{slugify(str(material['disciplina']), 70)}"
    lesson_id = str(material.get("aula_id") or "aula")
    lesson = f"{slugify(lesson_id, 24)}-{slugify(str(material['aula']), 45)}"
    title = slugify(str(material["titulo"]), 65)
    return texts_root / course_slug / discipline / lesson / f"{title}-{material_id[-12:]}.txt"


def _extract_text(pdf_path: Path, text_path: Path, executable: str, timeout: int) -> dict[str, Any]:
    text_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = text_path.with_name(f".{text_path.name}.{uuid.uuid4().hex}.tmp")
    extracted_at = now_iso()
    try:
        completed = subprocess.run(
            [executable, "-layout", "-enc", "UTF-8", str(pdf_path), str(temporary)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
            check=False,
        )
        if completed.returncode != 0:
            detail = completed.stderr.strip() or f"código de saída {completed.returncode}"
            raise RuntimeError(detail)
        if not temporary.is_file():
            raise RuntimeError("o extrator não produziu o arquivo de texto")
        text = temporary.read_text(encoding="utf-8", errors="replace")
        if not text.strip():
            raise RuntimeError("o PDF não produziu texto pesquisável")
        os.replace(temporary, text_path)
        return {
            "status": "ok",
            "extraido_em": extracted_at,
            "tamanho_texto_bytes": text_path.stat().st_size,
            "caracteres": len(text),
        }
    finally:
        temporary.unlink(missing_ok=True)


def _can_skip(
    previous: dict[str, Any] | None,
    pdf_hash: str,
    expected_text: Path,
    project_root: Path,
) -> bool:
    if not previous or previous.get("sha256") != pdf_hash:
        return False
    extraction = previous.get("extracao")
    if not isinstance(extraction, dict) or extraction.get("status") != "ok":
        return False
    if extraction.get("pdf_sha256") != pdf_hash:
        return False
    if extraction.get("texto") != _portable_path(expected_text, project_root):
        return False
    if not expected_text.is_file() or expected_text.stat().st_size < 1:
        return False
    recorded_size = extraction.get("tamanho_texto_bytes")
    return recorded_size is None or recorded_size == expected_text.stat().st_size


def _build_index(
    source: dict[str, Any],
    source_path: Path,
    records: list[dict[str, Any]],
    generated_at: str,
    project_root: Path,
) -> dict[str, Any]:
    disciplines: OrderedDict[str, dict[str, Any]] = OrderedDict()
    for material in records:
        discipline_key = str(material.get("disciplina_id") or material["disciplina"])
        discipline = disciplines.setdefault(
            discipline_key,
            {
                "id": material.get("disciplina_id"),
                "nome": material["disciplina"],
                "aulas": OrderedDict(),
            },
        )
        lesson_key = str(material.get("aula_id") or material["aula"])
        lesson = discipline["aulas"].setdefault(
            lesson_key,
            {
                "id": material.get("aula_id"),
                "nome": material["aula"],
                "titulo": material.get("titulo_aula"),
                "materiais": [],
            },
        )
        extraction = material["extracao"]
        lesson["materiais"].append(
            {
                "id": material["material_id"],
                "titulo": material["titulo"],
                "pdf": material["caminho_pdf"],
                "texto": extraction.get("texto"),
                "status_extracao": extraction["status"],
                "sha256": material.get("sha256"),
            }
        )

    discipline_list: list[dict[str, Any]] = []
    for discipline in disciplines.values():
        discipline["aulas"] = list(discipline["aulas"].values())
        discipline["total_aulas"] = len(discipline["aulas"])
        discipline["total_materiais"] = sum(
            len(lesson["materiais"]) for lesson in discipline["aulas"]
        )
        discipline_list.append(discipline)

    return {
        "schema_version": SCHEMA_VERSION,
        "tipo": "indice-materiais-estrategia",
        "gerado_em": generated_at,
        "manifesto_fonte": _portable_path(source_path, project_root),
        "curso": {
            "nome": source["curso"],
            "package_id": source.get("package_id"),
            "url_origem": source.get("url_origem"),
        },
        "total_disciplinas": len(discipline_list),
        "total_aulas": sum(len(item["aulas"]) for item in discipline_list),
        "total_materiais": len(records),
        "disciplinas": discipline_list,
    }


def process_materials(
    *,
    project_root: Path,
    source_manifest: Path | None,
    output_root: Path,
    texts_root: Path,
    limit: int | None,
    force: bool,
    timeout: int,
) -> ProcessingResult:
    project_root = project_root.resolve()
    source_path = _discover_manifest(project_root, source_manifest)
    source = _read_json(source_path)
    _validate_source(source, source_path)

    executable = shutil.which("pdftotext")
    if not executable:
        raise ProcessingError("pdftotext não encontrado; instale o pacote poppler-utils")

    output_root = output_root if output_root.is_absolute() else project_root / output_root
    texts_root = texts_root if texts_root.is_absolute() else project_root / texts_root
    course_slug = slugify(source_path.stem, 100)
    course_output = output_root.resolve() / course_slug
    processed_manifest_path = course_output / "manifesto.json"
    index_path = course_output / "indice.json"
    report_path = course_output / "relatorio.json"

    previous_by_id: dict[str, dict[str, Any]] = {}
    if processed_manifest_path.is_file():
        previous_data = _read_json(processed_manifest_path)
        previous_by_id = {
            item["material_id"]: item
            for item in previous_data.get("materiais", [])
            if isinstance(item, dict) and item.get("material_id")
        }

    generated_at = now_iso()
    records: list[dict[str, Any]] = []
    extraction_errors: list[dict[str, Any]] = []
    processed_count = 0
    skipped_count = 0
    pending_count = 0
    error_count = 0
    source_size_mismatches = 0
    source_hash_mismatches = 0
    original_name_fallbacks = 0

    for source_material in source["materiais"]:
        material_id = _material_id(source_material)
        pdf_path = _resolve_project_path(str(source_material["arquivo"]), project_root)
        text_path = _text_path(source_material, material_id, texts_root.resolve(), course_slug)
        pdf_portable = _portable_path(pdf_path, project_root)
        text_portable = _portable_path(text_path, project_root)
        original_name_from_source = source_material.get("nome_original")
        if not original_name_from_source:
            original_name_fallbacks += 1

        record: dict[str, Any] = {
            "material_id": material_id,
            "curso": source["curso"],
            "disciplina": source_material["disciplina"],
            "disciplina_id": source_material.get("curso_id"),
            "aula": source_material["aula"],
            "aula_id": source_material.get("aula_id"),
            "titulo_aula": source_material.get("titulo_aula"),
            "titulo": source_material["titulo"],
            "caminho_pdf": pdf_portable,
            "nome_original": original_name_from_source or pdf_path.name,
            "nome_original_confirmado": bool(original_name_from_source),
            "url_origem": source_material.get("url_origem"),
            "baixado_em": source_material["baixado_em"],
        }

        if not pdf_path.is_file():
            message = "PDF não encontrado"
            record.update({"tamanho_bytes": None, "sha256": None})
            record["extracao"] = {
                "status": "erro",
                "texto": text_portable,
                "tentado_em": generated_at,
                "erro": message,
            }
            extraction_errors.append(
                {"material_id": material_id, "pdf": pdf_portable, "erro": message}
            )
            records.append(record)
            error_count += 1
            continue

        size = pdf_path.stat().st_size
        pdf_hash = sha256_file(pdf_path)
        if source_material.get("tamanho_bytes") != size:
            source_size_mismatches += 1
        if source_material.get("sha256") != pdf_hash:
            source_hash_mismatches += 1
        record.update({"tamanho_bytes": size, "sha256": pdf_hash})
        previous = previous_by_id.get(material_id)

        if not force and _can_skip(previous, pdf_hash, text_path, project_root):
            record["extracao"] = dict(previous["extracao"])
            records.append(record)
            skipped_count += 1
            continue

        if limit is not None and processed_count + error_count >= limit:
            record["extracao"] = {
                "status": "pendente",
                "texto": text_portable,
                "pdf_sha256": pdf_hash,
            }
            records.append(record)
            pending_count += 1
            continue

        try:
            extraction = _extract_text(pdf_path, text_path, executable, timeout)
            extraction.update(
                {
                    "pdf_sha256": pdf_hash,
                    "texto": text_portable,
                    "extrator": "pdftotext",
                }
            )
            record["extracao"] = extraction
            processed_count += 1
        except (OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
            message = f"{type(exc).__name__}: {exc}"
            record["extracao"] = {
                "status": "erro",
                "texto": text_portable,
                "pdf_sha256": pdf_hash,
                "tentado_em": now_iso(),
                "erro": message,
            }
            extraction_errors.append(
                {"material_id": material_id, "pdf": pdf_portable, "erro": message}
            )
            error_count += 1
        records.append(record)

    summary = {
        "total_materiais": len(records),
        "processados": processed_count,
        "ignorados": skipped_count,
        "pendentes": pending_count,
        "erros": error_count,
    }
    processed_manifest = {
        "schema_version": SCHEMA_VERSION,
        "tipo": "manifesto-materiais-processados",
        "gerado_em": generated_at,
        "manifesto_fonte": _portable_path(source_path, project_root),
        "curso": source["curso"],
        "package_id": source.get("package_id"),
        "url_origem": source.get("url_origem"),
        "observacoes": {
            "pdfs_originais_modificados": False,
            "nome_original": (
                "Quando ausente no manifesto bruto, usa o nome local e "
                "nome_original_confirmado=false."
            ),
        },
        "resumo": summary,
        "materiais": records,
    }
    index = _build_index(source, source_path, records, generated_at, project_root)
    report = {
        "schema_version": SCHEMA_VERSION,
        "tipo": "relatorio-processamento-materiais",
        "iniciado_em": generated_at,
        "concluido_em": now_iso(),
        "manifesto_fonte": _portable_path(source_path, project_root),
        "manifesto_processado": _portable_path(processed_manifest_path, project_root),
        "indice": _portable_path(index_path, project_root),
        "validacao_manifesto_fonte": {
            "registros": len(records),
            "arquivos_ausentes": sum(
                1 for item in records if item["extracao"].get("erro") == "PDF não encontrado"
            ),
            "divergencias_tamanho": source_size_mismatches,
            "divergencias_sha256": source_hash_mismatches,
            "nomes_originais_nao_registrados": original_name_fallbacks,
        },
        "resumo": summary,
        "erros": extraction_errors,
    }

    _write_json_atomic(processed_manifest_path, processed_manifest)
    _write_json_atomic(index_path, index)
    _write_json_atomic(report_path, report)
    return ProcessingResult(processed_manifest_path, index_path, report_path, summary)
