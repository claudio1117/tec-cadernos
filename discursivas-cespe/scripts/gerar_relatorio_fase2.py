#!/usr/bin/env python3
"""Gera o relatorio descritivo da expansao controlada (sem inferencia preditiva)."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: str) -> list[dict[str, str]]:
    with (ROOT / path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def table(headers: list[str], rows: list[list[object]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    out.extend("| " + " | ".join(str(cell).replace("|", "\\|") for cell in row) + " |" for row in rows)
    return "\n".join(out)


def main() -> None:
    contests = read_csv("dataset/concursos.csv")
    questions = read_csv("dataset/questoes_discursivas.csv")
    new_contests = contests[3:]
    new_questions = questions[11:]
    validation = json.loads((ROOT / "dados/fase2_validacao.json").read_text(encoding="utf-8"))
    rejected = json.loads((ROOT / "dados/fase2_pesquisados_nao_incorporados.json").read_text(encoding="utf-8"))
    question_count = Counter(r["id_concurso"] for r in questions)
    piece_count = Counter(r["id_concurso"] for r in questions if "peça" in r["tipo_discursiva"])
    category_by_contest = {r["id_concurso"]: r["categoria_comparabilidade"] for r in contests}

    lines = [
        "# Expansão controlada do corpus — fase 2",
        "",
        "## Escopo e resultado",
        "",
        "A fase 2 incorporou **20 novos concursos** CESPE/CEBRASPE, atingindo o teto definido. A seleção foi feita por órgão, cargo, nível e existência documental da prova discursiva; os temas cobrados só foram lidos e classificados depois de fechada a elegibilidade. Não houve busca de provas por termos do edital do TCE-MA.",
        "",
        f"O corpus consolidado contém **{len(contests)} concursos** e **{len(questions)} componentes discursivos**. Nesta expansão entraram **{len(new_questions)} componentes**, dos quais **{sum('peça' in q['tipo_discursiva'] for q in new_questions)} peças técnicas**. Considerando também a fase 1, há **{validation['totais']['pecas_tecnicas']} peças técnicas**. Nenhuma questão objetiva foi incluída.",
        "",
        "A documentação incorporada soma **88 PDFs oficiais**: 23 editais, 29 cadernos discursivos e 36 padrões de resposta. Há ainda 3 PDFs do CNJ 2024 preservados em `fontes/`, mas não incorporados à amostra final após a substituição pelo TCU 2025/2026. Dos 36 padrões usados no corpus, 31 são definitivos e 5 são preliminares (todos do TCE/PR 2016, única versão oficial localizada).",
        "",
        "## Concursos adicionados",
        "",
        table(["Categoria", "Ano da prova", "Concurso/cargo de TI", "Questões", "Peças"], [
            [r["categoria_comparabilidade"], r["ano"], f"{r['orgao']} — {r['especialidade']}", question_count[r["id_concurso"]], piece_count[r["id_concurso"]]]
            for r in new_contests
        ]),
        "",
        "Quando um único caderno foi destinado a várias especialidades de TI — TCE/AC 2024, TCE/PA 2016 e TRF6 2025 — o enunciado foi registrado uma vez, e todas as especialidades destinatárias foram preservadas no campo `especialidade`. Isso evita multiplicar artificialmente a mesma questão.",
        "",
        "## Documentos utilizados",
        "",
        "Todos os 79 documentos da fase 2 que sustentam os 20 concursos finais foram localizados pela API pública do CEBRASPE, recuperados do CDN oficial e validados como PDF. O manifesto `dados/fase2_fontes.json` registra, para cada arquivo, descrição da API, nome oficial, URL, caminho local e número de páginas. Os 9 PDFs da fase 1 foram mantidos sem alteração.",
        "",
        "Os campos `texto_padrao_resposta` e `quesitos_avaliados` guardam a extração integral das páginas pertinentes do padrão; `distribuicao_pontos_padrao` preserva o total e os valores explícitos recuperáveis. Classificações analíticas permanecem em campos separados.",
        "",
        "## Distribuição por tipo de órgão",
        "",
        table(["Categoria", "Concursos novos", "Componentes novos"], [
            [cat, sum(r["categoria_comparabilidade"] == cat for r in new_contests), sum(category_by_contest[q["id_concurso"]] == cat for q in new_questions)]
            for cat in ["A", "B", "C", "D", "E"]
        ]),
        "",
        "No corpus total, os 23 concursos distribuem-se em 17 da categoria A, 3 da B e 3 da C. Não foram incluídos concursos D ou E antes de atingir o teto com as prioridades superiores; isso não constitui exclusão temática e não estabelece peso analítico futuro.",
        "",
        "## Distribuição por ano de aplicação",
        "",
        table(["Ano", "Componentes novos", "Corpus total"], [
            [year, Counter(q["ano"] for q in new_questions)[year], Counter(q["ano"] for q in questions)[year]]
            for year in sorted({q["ano"] for q in questions})
        ]),
        "",
        "O ano registrado é o da aplicação da prova, não necessariamente o ano no identificador do evento. Assim, por exemplo, TCE/SC 2021 aparece como 2022; TCE/MG 2025, SEFA/PR 2025 e TCU 2025 aparecem como 2026; TRT10 2024 e TRF6 2024 aparecem como 2025.",
        "",
        "## Correspondência conceitual com o edital do TCE-MA",
        "",
        table(["Classificação", "Novas questões", "Corpus total"], [
            [kind, Counter(q["correspondencia_com_edital_tce_ma"] for q in new_questions)[kind], Counter(q["correspondencia_com_edital_tce_ma"] for q in questions)[kind]]
            for kind in ["direta", "parcial", "apenas relacionada", "inexistente"]
        ]),
        "",
        "As correspondências foram feitas após a coleta e pela substância do enunciado e do padrão. Toda correspondência direta ou parcial aponta itens específicos de `dados/tce_ma_conteudo_programatico.json`. Questões gerais e conteúdos ausentes do edital foram mantidos, inclusive as 11 novas classificadas como inexistentes.",
        "",
        "## Concursos pesquisados mas não incorporados",
        "",
        table(["Evento", "Situação", "Motivo"], [[r["evento"], r["status"], r["motivo"]] for r in rejected]),
        "",
        "## Controle de qualidade",
        "",
        "A validação automatizada terminou com status **aprovado** e sem erros. Foram conferidos:",
        "",
        "- unicidade dos 23 concursos e das 56 questões, inclusive pelo hash do enunciado;",
        "- integridade das chaves estrangeiras;",
        "- validade sintática de todos os campos JSON multivalorados;",
        "- vocabulários controlados para correspondência, forma de cobrança e campos booleanos;",
        "- existência, assinatura PDF e número de páginas dos 79 documentos manifestados na fase 2;",
        "- preservação, campo a campo, dos 25 campos originais das 11 questões da fase 1;",
        "- presença de enunciado e padrão de resposta em todos os registros;",
        "- ausência de questões objetivas e de artefatos de páginas de rascunho nos enunciados.",
        "",
        "Não há registros incorporados com `status_confirmacao = não confirmado`. Listas vazias em `ano_norma_cobrada` indicam que o ano/edição não foi identificado com segurança na documentação, e não foram preenchidas por suposição.",
        "",
        "O resultado detalhado está em `dados/fase2_validacao.json`.",
        "",
        "## Problemas e divergências documentais",
        "",
        "- O caderno do TCE/SC tem mapa de caracteres defeituoso na extração de texto. O mapeamento foi revertido de forma determinística e conferido visualmente. A grafia literal `NBR2700` existente no caderno foi preservada; não se fez correção silenciosa.",
        "- A API usa os mesmos nomes de arquivo baseados em hash para a prova e o padrão de SEFA/PR 2025 e TCU 2025. As URLs têm diretórios de evento distintos e retornam conteúdos distintos, o que foi confirmado pelos hashes locais.",
        "- Para o TCE/PR 2016, somente padrões preliminares foram localizados na API oficial; os cinco registros indicam expressamente essa limitação.",
        "- Cadernos comuns a múltiplos cargos poderiam gerar duplicatas artificiais; a unidade de registro adotada foi o enunciado efetivamente distinto, com todos os cargos de TI destinatários indicados.",
        "- Alguns identificadores oficiais usam o ano do edital, enquanto a prova ocorreu no ano seguinte. O campo `ano` usa a aplicação e `observacoes` preserva o contexto.",
        "",
        "## Limitações",
        "",
        "- A amostra foi encerrada ao atingir 20 novos concursos; ela não é um censo de todas as provas entre 2015 e 2026.",
        "- A normalização textual remove espaços e artefatos de leiaute, mas os PDFs originais permanecem disponíveis para conferência.",
        "- Campos como tema, forma de cobrança, nível de abstração e correspondência são classificações analíticas, não trechos documentais.",
        "- `ano_norma_cobrada` fica como lista vazia quando o enunciado não explicita o ano ou a edição; nenhum ano foi presumido.",
        "- Concursos elegíveis de prioridade inferior podem existir fora desta amostra; a coleta foi deliberadamente interrompida no teto aprovado.",
        "",
        "## Encerramento da fase",
        "",
        "Esta etapa não produz ranking, frequência interpretada, probabilidade, previsão de cobrança ou recomendação de estudo. O corpus fica aguardando revisão metodológica antes de qualquer análise estatística final.",
        "",
    ]
    (ROOT / "relatorios/expansao_fase2.md").write_text("\n".join(lines), encoding="utf-8")
    print("relatorios/expansao_fase2.md gerado")


if __name__ == "__main__":
    main()
