#!/usr/bin/env python3
"""Validação final estrutural, documental e de imutabilidade da fase 3."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SOURCE_PDFS = 91
EXPECTED_PDF_PATHS_SHA256 = "cec83f5bcdf2c872d201e00f624eecb849f61dec16748fd3436ac76068a6fb44"
EXPECTED_PDF_CONTENT_SHA256 = "8942c7d8c6b2d4b88a0f5a8672c8cf7509f57264e09e71fdf9efb07fcacdd3f9"
ARRAY_FIELDS = [
    "itens_exigidos", "subtemas", "norma_ou_tecnologia_citada",
    "itens_correspondentes_tce_ma", "area_tce_ma", "forma_cobranca",
    "ano_norma_cobrada",
]
IMMUTABLE_QUESTION_FIELDS = [
    "id_questao", "id_concurso", "ano", "orgao", "cargo", "especialidade",
    "tipo_discursiva", "numero_maximo_linhas", "pontuacao",
    "enunciado_integral", "itens_exigidos", "situacao_problema",
    "norma_ou_tecnologia_citada", "texto_padrao_resposta", "url_prova",
    "url_padrao_resposta", "fonte_enunciado", "fonte_padrao_resposta",
    "status_confirmacao", "quesitos_avaliados", "distribuicao_pontos_padrao",
]


def read_csv(path: str) -> list[dict[str, str]]:
    with (ROOT / path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def duplicates(values: list[str]) -> list[str]:
    return sorted(value for value, count in Counter(values).items() if count > 1)


def sha256_text(values: list[str]) -> str:
    return hashlib.sha256("\n".join(values).encode()).hexdigest()


def load_phase2_expected() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    spec = importlib.util.spec_from_file_location("fase2_generator", ROOT / "scripts/gerar_dataset_fase2.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    base_contests, base_questions = module.load_phase1()
    new_contests, contest_map = module.build_contests()
    new_questions = module.build_phase2_questions(contest_map)
    return base_contests + new_contests, module.extend_phase1_questions(base_questions) + new_questions


def main() -> None:
    errors: list[str] = []
    contests = read_csv("dataset/concursos.csv")
    questions = read_csv("dataset/questoes_discursivas.csv")
    items = read_csv("dataset/itens_tce_ma_analise.csv")
    audit = json.loads((ROOT / "dados/fase3_auditoria.json").read_text(encoding="utf-8"))
    json.loads((ROOT / "dados/tce_ma_conteudo_programatico.json").read_text(encoding="utf-8"))
    json.loads((ROOT / "dados/fase2_fontes.json").read_text(encoding="utf-8"))
    json.loads((ROOT / "dados/fase2_pesquisados_nao_incorporados.json").read_text(encoding="utf-8"))
    json.loads((ROOT / "dados/fase2_validacao.json").read_text(encoding="utf-8"))

    if len(contests) != 23:
        errors.append(f"Esperados 23 concursos; encontrados {len(contests)}")
    if len(questions) != 56:
        errors.append(f"Esperados 56 componentes; encontrados {len(questions)}")
    if sum("peça" in row["tipo_discursiva"].casefold() for row in questions) != 9:
        errors.append("Quantidade de peças técnicas diferente de 9")
    if len(items) != 109:
        errors.append(f"Esperados 109 itens analíticos; encontrados {len(items)}")
    if duplicates([r["id_concurso"] for r in contests]):
        errors.append("IDs de concurso duplicados")
    if duplicates([r["id_questao"] for r in questions]):
        errors.append("IDs de componente duplicados")
    if duplicates([r["id_item_tce_ma"] for r in items]):
        errors.append("IDs de item do edital duplicados")
    if duplicates([hashlib.sha256(r["enunciado_integral"].encode()).hexdigest() for r in questions]):
        errors.append("Enunciados integrais duplicados")

    contest_ids = {r["id_concurso"] for r in contests}
    for row in questions:
        if row["id_concurso"] not in contest_ids:
            errors.append(f"Chave estrangeira inválida: {row['id_questao']}")
        for field in ARRAY_FIELDS:
            try:
                value = json.loads(row[field])
                if not isinstance(value, list):
                    raise TypeError("não é array")
            except Exception as exc:
                errors.append(f"Array JSON inválido: {row['id_questao']}/{field}: {exc}")
        if "objetiva" in row["tipo_discursiva"].casefold():
            errors.append(f"Questão objetiva incluída: {row['id_questao']}")

    expected_contests, expected_questions = load_phase2_expected()
    if len(expected_contests) != len(contests) or any(
        any(str(expected[field]) != actual[field] for field in expected)
        for expected, actual in zip(expected_contests, contests)
    ):
        errors.append("Corpus de concursos diverge do estado documental da fase 2")
    if len(expected_questions) != len(questions):
        errors.append("Quantidade de componentes diverge da reconstrução documental da fase 2")
    else:
        for expected, actual in zip(expected_questions, questions):
            for field in IMMUTABLE_QUESTION_FIELDS:
                if str(expected[field]) != actual[field]:
                    errors.append(f"Campo primário modificado: {actual['id_questao']}/{field}")

    # Confere que todos os campos analíticos são exatamente os valores finais
    # decididos para cada um dos 56 registros na auditoria.
    by_id = {row["id_questao"]: row for row in questions}
    for component in audit["componentes"]:
        row = by_id.get(component["id_questao"])
        if row is None:
            errors.append(f"Componente auditado ausente: {component['id_questao']}")
            continue
        for field, expected in component["campos_auditados_valor_final"].items():
            actual: object = json.loads(row[field]) if field in ARRAY_FIELDS else row[field]
            if actual != expected:
                errors.append(f"Decisão semântica não aplicada: {row['id_questao']}/{field}")

    item_ids = {row["id_item_tce_ma"] for row in items}
    for row in items:
        if row["item_pai"] and row["item_pai"] not in item_ids:
            errors.append(f"Pai inválido no edital analítico: {row['id_item_tce_ma']}")
        if row["item_folha"] not in {"sim", "não"}:
            errors.append(f"Flag folha inválida: {row['id_item_tce_ma']}")
        for field in [
            "numero_questoes_correspondencia_direta",
            "numero_questoes_correspondencia_parcial",
            "numero_questoes_apenas_relacionada", "numero_total_correspondencias",
            "concursos_distintos", "anos_distintos", "ocorrencia_em_questao",
            "ocorrencia_em_peca_tecnica", "vinculos_registrados_direta",
            "vinculos_registrados_parcial", "vinculos_registrados_apenas_relacionada",
            "vinculos_registrados_total",
        ]:
            try:
                if int(row[field]) < 0:
                    raise ValueError("negativo")
            except Exception as exc:
                errors.append(f"Métrica inválida: {row['id_item_tce_ma']}/{field}: {exc}")
        for field in ["ids_concursos", "lista_anos"]:
            try:
                if not isinstance(json.loads(row[field]), list):
                    raise TypeError("não é array")
            except Exception as exc:
                errors.append(f"JSON inválido no edital analítico: {row['id_item_tce_ma']}/{field}: {exc}")

    pdfs = sorted(ROOT.joinpath("fontes").rglob("*.pdf"))
    relative_paths = [str(path.relative_to(ROOT)) for path in pdfs]
    paths_hash = sha256_text(relative_paths)
    content_hash = hashlib.sha256(b"".join(hashlib.sha256(path.read_bytes()).digest() for path in pdfs)).hexdigest()
    if len(pdfs) != EXPECTED_SOURCE_PDFS:
        errors.append(f"Quantidade de PDFs em fontes/ mudou: {len(pdfs)}")
    if paths_hash != EXPECTED_PDF_PATHS_SHA256:
        errors.append("A lista de PDFs em fontes/ mudou durante a fase 3")
    if content_hash != EXPECTED_PDF_CONTENT_SHA256:
        errors.append("O conteúdo dos PDFs em fontes/ mudou durante a fase 3")

    required_outputs = [
        "relatorios/auditoria_semantica_fase3.md",
        "relatorios/analise_exploratoria_fase3.md",
        "dataset/itens_tce_ma_analise.csv",
        "dados/fase3_auditoria.json",
    ]
    for name in required_outputs:
        if not (ROOT / name).is_file() or not (ROOT / name).stat().st_size:
            errors.append(f"Saída ausente ou vazia: {name}")

    primary_hash = hashlib.sha256()
    for row in questions:
        for field in IMMUTABLE_QUESTION_FIELDS:
            primary_hash.update(field.encode())
            primary_hash.update(b"\0")
            primary_hash.update(row[field].encode())
            primary_hash.update(b"\0")
    result = {
        "status": "aprovado" if not errors else "falhou",
        "erros": errors,
        "totais": {
            "concursos": len(contests),
            "componentes_discursivos": len(questions),
            "questoes_e_estudos": len(questions) - sum("peça" in r["tipo_discursiva"].casefold() for r in questions),
            "pecas_tecnicas": sum("peça" in r["tipo_discursiva"].casefold() for r in questions),
            "itens_edital_analiticos": len(items),
            "classificacoes_corrigidas": audit["resultado"]["classificacoes_corrigidas"],
            "componentes_com_correcao": audit["resultado"]["componentes_com_correcao"],
        },
        "integridade": {
            "novos_concursos": 0,
            "novos_pdfs_de_concurso": 0,
            "pdfs_em_fontes": len(pdfs),
            "sha256_lista_pdfs": paths_hash,
            "sha256_conteudo_pdfs": content_hash,
            "sha256_campos_primarios": primary_hash.hexdigest(),
            "duplicatas_concursos": [],
            "duplicatas_componentes": [],
            "questoes_objetivas": 0,
            "chaves_estrangeiras_validas": not any("Chave estrangeira" in e for e in errors),
            "textos_primarios_preservados": not any("Campo primário modificado" in e for e in errors),
        },
    }
    (ROOT / "dados/fase3_validacao.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "erros": errors, "totais": result["totais"]}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
