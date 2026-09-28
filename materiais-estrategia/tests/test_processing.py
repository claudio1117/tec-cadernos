from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from estrategia.processing import _can_skip, _material_id, process_materials, slugify


class ProcessingHelpersTest(unittest.TestCase):
    def test_slugify_removes_accents_and_normalizes_spaces(self) -> None:
        self.assertEqual(slugify("Aula: Gestão Pública / 01"), "aula-gestao-publica-01")

    def test_material_id_is_stable(self) -> None:
        material = {
            "curso_id": "10",
            "aula_id": "20",
            "titulo": "Livro eletrônico",
            "arquivo": "downloads/a.pdf",
        }
        first = _material_id(material)
        second = _material_id(dict(material))
        self.assertEqual(first, second)
        self.assertTrue(first.startswith("20-"))

    def test_incremental_skip_requires_matching_hash_and_text(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            text = root / "textos" / "aula.txt"
            text.parent.mkdir()
            text.write_text("conteúdo", encoding="utf-8")
            pdf_hash = hashlib.sha256(b"pdf").hexdigest()
            previous = {
                "sha256": pdf_hash,
                "extracao": {
                    "status": "ok",
                    "pdf_sha256": pdf_hash,
                    "texto": "textos/aula.txt",
                    "tamanho_texto_bytes": text.stat().st_size,
                },
            }
            self.assertTrue(_can_skip(previous, pdf_hash, text, root))
            self.assertFalse(_can_skip(previous, "0" * 64, text, root))
            text.unlink()
            self.assertFalse(_can_skip(previous, pdf_hash, text, root))

    def test_processing_continues_after_one_extraction_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifests = root / "data" / "manifests"
            downloads = root / "downloads"
            manifests.mkdir(parents=True)
            downloads.mkdir()
            for name in ("falha.pdf", "sucesso.pdf"):
                (downloads / name).write_bytes(b"%PDF-conteudo-de-teste")
            source = {
                "curso": "Curso de teste",
                "materiais": [
                    {
                        "disciplina": "Disciplina",
                        "aula": f"Aula {index}",
                        "aula_id": str(index),
                        "titulo": "Livro",
                        "arquivo": f"downloads/{name}",
                        "baixado_em": "2026-01-01T12:00:00-03:00",
                    }
                    for index, name in enumerate(("falha.pdf", "sucesso.pdf"), 1)
                ],
            }
            source_path = manifests / "curso.json"
            source_path.write_text(json.dumps(source), encoding="utf-8")

            def fake_extract(pdf: Path, text: Path, _executable: str, _timeout: int):
                if pdf.name == "falha.pdf":
                    raise RuntimeError("falha simulada")
                text.parent.mkdir(parents=True, exist_ok=True)
                text.write_text("texto extraído", encoding="utf-8")
                return {
                    "status": "ok",
                    "extraido_em": "2026-01-02T12:00:00-03:00",
                    "tamanho_texto_bytes": text.stat().st_size,
                    "caracteres": 14,
                }

            with (
                patch("estrategia.processing.shutil.which", return_value="pdftotext"),
                patch("estrategia.processing._extract_text", side_effect=fake_extract),
            ):
                result = process_materials(
                    project_root=root,
                    source_manifest=source_path,
                    output_root=root / "data" / "processados",
                    texts_root=root / "textos",
                    limit=None,
                    force=False,
                    timeout=10,
                )

            self.assertEqual(result.summary["processados"], 1)
            self.assertEqual(result.summary["erros"], 1)
            processed = json.loads(result.manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(
                [item["extracao"]["status"] for item in processed["materiais"]],
                ["erro", "ok"],
            )


if __name__ == "__main__":
    unittest.main()
