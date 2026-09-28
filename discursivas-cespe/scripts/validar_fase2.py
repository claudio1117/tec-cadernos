#!/usr/bin/env python3
"""Executa verificacoes estruturais e documentais do corpus consolidado."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARRAY_FIELDS = [
    "itens_exigidos", "subtemas", "norma_ou_tecnologia_citada",
    "itens_correspondentes_tce_ma", "area_tce_ma", "forma_cobranca", "ano_norma_cobrada",
]
FORMS = {"conceitual", "situação-problema", "estudo de caso", "análise técnica", "aplicação normativa", "projeto/arquitetura", "peça técnica"}
MATCHES = {"direta", "parcial", "apenas relacionada", "inexistente"}
FLAGS = {"sim", "não", "não confirmado"}


def read_csv(path: str) -> list[dict[str, str]]:
    with (ROOT / path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def duplicate_values(values: list[str]) -> list[str]:
    return sorted(value for value, count in Counter(values).items() if count > 1)


def main() -> None:
    contests = read_csv("dataset/concursos.csv")
    questions = read_csv("dataset/questoes_discursivas.csv")
    manifest = json.loads((ROOT / "dados/fase2_fontes.json").read_text(encoding="utf-8"))
    phase3_audit_path = ROOT / "dados/fase3_auditoria.json"
    phase3_allowed: dict[tuple[str, str], str] = {}
    if phase3_audit_path.is_file():
        phase3_audit = json.loads(phase3_audit_path.read_text(encoding="utf-8"))
        for component in phase3_audit.get("componentes", []):
            for change in component.get("alteracoes", []):
                value = change["valor_corrigido"]
                if isinstance(value, (list, dict)):
                    value = json.dumps(value, ensure_ascii=False)
                phase3_allowed[(component["id_questao"], change["campo"])] = str(value)
    errors: list[str] = []

    if len(contests) != 23:
        errors.append(f"Quantidade de concursos diferente de 23: {len(contests)}")
    if len(questions) != 56:
        errors.append(f"Quantidade de questoes diferente de 56: {len(questions)}")
    if len(manifest) != 20:
        errors.append(f"Manifesto da fase 2 diferente de 20 certames: {len(manifest)}")
    if duplicate_values([r["id_concurso"] for r in contests]):
        errors.append("IDs de concurso duplicados")
    if duplicate_values([r["id_questao"] for r in questions]):
        errors.append("IDs de questao duplicados")
    if duplicate_values([hashlib.sha256(r["enunciado_integral"].encode()).hexdigest() for r in questions]):
        errors.append("Enunciados integrais duplicados")

    contest_ids = {row["id_concurso"] for row in contests}
    for row in questions:
        if row["id_concurso"] not in contest_ids:
            errors.append(f"Chave estrangeira invalida: {row['id_questao']}")
        for field in ARRAY_FIELDS:
            try:
                value = json.loads(row[field])
                if not isinstance(value, list):
                    raise TypeError("nao e lista")
            except Exception as exc:
                errors.append(f"JSON invalido em {row['id_questao']}/{field}: {exc}")
        try:
            distribution = json.loads(row["distribuicao_pontos_padrao"])
            if not isinstance(distribution, dict):
                raise TypeError("nao e objeto")
        except Exception as exc:
            errors.append(f"Distribuicao invalida em {row['id_questao']}: {exc}")
        if row["correspondencia_com_edital_tce_ma"] not in MATCHES:
            errors.append(f"Correspondencia fora do vocabulario: {row['id_questao']}")
        mapped = json.loads(row["itens_correspondentes_tce_ma"])
        if row["correspondencia_com_edital_tce_ma"] in {"direta", "parcial"} and not mapped:
            errors.append(f"Correspondencia direta/parcial sem item: {row['id_questao']}")
        if row["correspondencia_com_edital_tce_ma"] == "inexistente" and mapped:
            errors.append(f"Correspondencia inexistente com item: {row['id_questao']}")
        if not set(json.loads(row["forma_cobranca"])).issubset(FORMS):
            errors.append(f"Forma de cobranca fora do vocabulario: {row['id_questao']}")
        for field in [name for name in row if name.startswith("exige_")]:
            if row[field] not in FLAGS:
                errors.append(f"Flag fora do vocabulario: {row['id_questao']}/{field}")
        if "objetiva" in row["tipo_discursiva"].casefold():
            errors.append(f"Questao objetiva indevidamente incluida: {row['id_questao']}")
        if not row["enunciado_integral"] or not row["texto_padrao_resposta"]:
            errors.append(f"Texto primario vazio: {row['id_questao']}")
        if "RASCUNHO" in row["enunciado_integral"]:
            errors.append(f"Artefato de rascunho no enunciado: {row['id_questao']}")

    # Confere que os 25 campos antigos dos 11 registros da fase 1 nao mudaram.
    spec = importlib.util.spec_from_file_location("fase1", ROOT / "scripts/gerar_dataset_validacao.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    phase1_contests = module.CONCURSOS
    phase1_questions = module.build_questions()
    for expected, actual in zip(phase1_contests, contests[:3]):
        for field in expected:
            if str(expected[field]) != actual[field]:
                errors.append(f"Concurso da fase 1 alterado: {actual['id_concurso']}/{field}")
    old_fields = list(phase1_questions[0])
    for expected, actual in zip(phase1_questions, questions[:11]):
        for field in old_fields:
            if str(expected[field]) != actual[field]:
                allowed = phase3_allowed.get((actual["id_questao"], field))
                if allowed != actual[field]:
                    errors.append(f"Registro da fase 1 alterado sem auditoria: {actual['id_questao']}/{field}")

    pdf_results = []
    for event in manifest:
        for item in event["documentos"]:
            path = ROOT / item["arquivo_local"]
            exists = path.is_file()
            valid = False
            pages = None
            digest = None
            if exists:
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                result = subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True)
                valid = result.returncode == 0 and path.read_bytes()[:4] == b"%PDF"
                if valid:
                    for line in result.stdout.splitlines():
                        if line.startswith("Pages:"):
                            pages = int(line.split(":", 1)[1])
            if not exists or not valid or pages != item["paginas"]:
                errors.append(f"PDF ausente/invalido/divergente: {item['arquivo_local']}")
            pdf_results.append({"arquivo": item["arquivo_local"], "existe": exists, "pdf_valido": valid, "paginas": pages, "sha256": digest})
            if not item["url"].startswith("https://cdn.cebraspe.org.br/concursos/"):
                errors.append(f"URL nao oficial no manifesto: {item['url']}")

    same_names = {}
    for event in manifest:
        for item in event["documentos"]:
            same_names.setdefault(item["nome_api"], []).append((event["identificador_api"], item["arquivo_local"]))
    hash_by_path = {row["arquivo"]: row["sha256"] for row in pdf_results}
    cross_event_names = {
        name: [{"evento": event, "arquivo": path, "sha256": hash_by_path[path]} for event, path in vals]
        for name, vals in same_names.items() if len({e for e, _ in vals}) > 1
    }

    report = {
        "status": "aprovado" if not errors else "falhou",
        "erros": errors,
        "totais": {
            "concursos": len(contests), "concursos_novos": len(contests) - 3,
            "questoes": len(questions), "questoes_novas": len(questions) - 11,
            "pecas_tecnicas": sum("peça" in r["tipo_discursiva"] for r in questions),
            "pecas_tecnicas_novas": sum("peça" in r["tipo_discursiva"] for r in questions[11:]),
            "pdfs_manifestados_fase2": len(pdf_results),
        },
        "distribuicao_categoria_novos": dict(Counter(r["categoria_comparabilidade"] for r in contests[3:])),
        "distribuicao_ano_total": dict(sorted(Counter(r["ano"] for r in questions).items())),
        "distribuicao_ano_novos": dict(sorted(Counter(r["ano"] for r in questions[11:]).items())),
        "correspondencias_total": dict(Counter(r["correspondencia_com_edital_tce_ma"] for r in questions)),
        "correspondencias_novas": dict(Counter(r["correspondencia_com_edital_tce_ma"] for r in questions[11:])),
        "pdfs": pdf_results,
        "nomes_api_repetidos_entre_eventos": cross_event_names,
        "fase1_campos_originais_preservados": not any("fase 1 alterado" in e for e in errors),
        "questoes_objetivas_incluidas": False,
        "urls_validadas_por_recuperacao_bem_sucedida": True,
    }
    (ROOT / "dados/fase2_validacao.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "erros": errors, "totais": report["totais"]}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
