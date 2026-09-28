#!/usr/bin/env python3
"""Gera a unidade analítica do edital e a análise descritiva da fase 3."""

from __future__ import annotations

import csv
import json
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AREAS = [
    "ENGENHARIA DE DADOS", "ENGENHARIA DE SOFTWARE", "ANÁLISE DE DADOS",
    "INTELIGÊNCIA ARTIFICIAL", "ARQUITETURA DE SOFTWARE",
    "GESTÃO E GOVERNANÇA DE TI", "CONTRATAÇÕES DE TI",
]
FORMS = [
    "conceitual", "situação-problema", "estudo de caso", "análise técnica",
    "aplicação normativa", "projeto/arquitetura", "peça técnica",
]
FLAGS = [
    "exige_memorizacao_normativa", "exige_aplicacao_pratica",
    "exige_proposta_solucao", "exige_comparacao",
    "exige_explicacao_conceitual", "exige_calculo", "exige_codigo",
    "exige_diagrama", "exige_conhecimento_legislacao",
]
MATCH_ORDER = ["direta", "parcial", "apenas relacionada", "inexistente"]
FORM_ORDER = {name: i for i, name in enumerate(FORMS)}


def read_csv(path: str) -> list[dict[str, str]]:
    with (ROOT / path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def arr(row: dict[str, str], field: str) -> list[object]:
    return json.loads(row[field])


def pct(n: int, d: int) -> str:
    return f"{100 * n / d:.1f}%".replace(".", ",") if d else "0,0%"


def number(text: str) -> str:
    match = re.match(r"^(\d+(?:\.\d+)*)\.?\s+", text)
    return match.group(1) if match else ""


def is_piece(row: dict[str, str]) -> bool:
    return "peça" in row["tipo_discursiva"].casefold()


def period(year: int) -> str:
    if year <= 2018:
        return "2015–2018"
    if year <= 2022:
        return "2019–2022"
    return "2023–2026"


def thematic_groups(row: dict[str, str]) -> set[str]:
    blob = " ".join([
        row["tema_principal"], *map(str, arr(row, "subtemas")),
        *map(str, arr(row, "norma_ou_tecnologia_citada")),
    ]).casefold()
    groups: set[str] = set()
    if "contrata" in blob or "licita" in blob or "sisp" in blob or "saas" in blob:
        groups.add("Contratações e gestão contratual de TI")
    if any(k in blob for k in ["segurança", "ciber", "autentica", "certific", "criptograf", "vulnerab", "devsecops", "iso/iec 270"]):
        groups.add("Segurança da informação e cibersegurança")
    if any(k in blob for k in ["scrum", "kanban", "extreme programming", "xp", "ágil", "pmbok"]):
        groups.add("Métodos ágeis e gestão de projetos")
    if any(k in blob for k in ["itil", "cobit", "governança", "gestão de serviços", "gerenciamento de incidentes", "gerenciamento de problemas"]):
        groups.add("Governança e gestão de serviços de TI")
    if any(k in blob for k in ["mineração", "modelagem de dados", "etl", "elt", "olap", "hadoop", "processamento de dados", "modelo preditivo", "integração e ingestão"]):
        groups.add("Engenharia e análise de dados")
    if any(k in blob for k in ["inteligência artificial", "aprendizado de máquina", "deep learning", "rede neural", "mlops", "linguagem natural"]):
        groups.add("Inteligência artificial e aprendizado de máquina")
    if any(k in blob for k in ["engenharia de software", "processos de engenharia", "desenvolvimento seguro", "devsecops", "tdd", "ddd", "qualidade de software"]):
        groups.add("Engenharia de software e práticas de desenvolvimento")
    if any(k in blob for k in ["modelo osi", "tcp/ip", "ipv4", "ipv6", "congestionamento tcp", "estrutura de rede", "infraestrutura"]):
        groups.add("Infraestrutura e redes")
    if row["conhecimento_geral_ou_especifico"] == "geral" and any(k in blob for k in ["controle", "tribunal de contas", "auditoria", "responsabilidade civil", "independência"]):
        groups.add("Controle externo, auditoria geral e direito público")
    if any(k in blob for k in ["sustent", "climát"]):
        groups.add("Sustentabilidade e emergência climática")
    return groups


def build_items(questions: list[dict[str, str]]) -> list[dict[str, object]]:
    source = json.loads((ROOT / "dados/tce_ma_conteudo_programatico.json").read_text(encoding="utf-8"))
    items: list[dict[str, object]] = []
    stacks: dict[str, dict[int, int]] = defaultdict(dict)
    last_area = None
    for idx, item in enumerate(source, 1):
        area = item["area"]
        if area != last_area:
            stacks[area] = {}
            last_area = area
        num = number(item["texto_original_edital"])
        level = num.count(".") + 1 if num else 1
        parent_index = None
        if level > 1:
            candidate = stacks[area].get(level - 1)
            if candidate is not None:
                parent_num = str(items[candidate]["numero_item"])
                if num.startswith(parent_num + "."):
                    parent_index = candidate
        for old_level in [x for x in stacks[area] if x >= level]:
            del stacks[area][old_level]
        stacks[area][level] = len(items)
        record = {
            "id_item_tce_ma": f"TCE-MA-{idx:03d}",
            "area": area,
            "numero_item": num,
            "texto_original": item["texto_original_edital"],
            "nivel_hierarquico": level,
            "item_pai": "",
            "item_folha": "sim",
            "pagina_edital": item["pagina_edital"],
            "_parent_index": parent_index,
        }
        items.append(record)
        if parent_index is not None:
            record["item_pai"] = items[parent_index]["id_item_tce_ma"]
            items[parent_index]["item_folha"] = "não"

    key_to_index = {f"{item['area']} — {item['texto_original']}": i for i, item in enumerate(items)}
    metrics = [
        {"direta": set(), "parcial": set(), "apenas relacionada": set(), "all": set(),
         "contests": set(), "years": set(), "questions": set(), "pieces": set(),
         "raw_direta": set(), "raw_parcial": set(), "raw_apenas relacionada": set(), "raw_all": set()}
        for _ in items
    ]

    def ancestors(index: int) -> set[int]:
        result: set[int] = set()
        parent_index = items[index]["_parent_index"]
        while parent_index is not None:
            result.add(parent_index)
            parent_index = items[parent_index]["_parent_index"]
        return result

    for row in questions:
        mapped_indices = []
        for key in arr(row, "itens_correspondentes_tce_ma"):
            if key not in key_to_index:
                raise ValueError(f"Mapeamento não encontrado no edital: {row['id_questao']} / {key}")
            mapped_indices.append(key_to_index[key])
        # Retém a associação mais específica: um pai não é contado de novo se
        # um descendente já representa o mesmo fenômeno naquela questão.
        ancestor_of_selected = set().union(*(ancestors(i) for i in mapped_indices)) if mapped_indices else set()
        canonical = [i for i in mapped_indices if i not in ancestor_of_selected]
        for index in mapped_indices:
            raw_bucket = metrics[index]
            raw_match = row["correspondencia_com_edital_tce_ma"]
            if raw_match != "inexistente":
                raw_bucket[f"raw_{raw_match}"].add(row["id_questao"])
                raw_bucket["raw_all"].add(row["id_questao"])
        for index in canonical:
            bucket = metrics[index]
            match = row["correspondencia_com_edital_tce_ma"]
            if match != "inexistente":
                bucket[match].add(row["id_questao"])
                bucket["all"].add(row["id_questao"])
                bucket["contests"].add(row["id_concurso"])
                bucket["years"].add(int(row["ano"]))
                bucket["pieces" if is_piece(row) else "questions"].add(row["id_questao"])

    output: list[dict[str, object]] = []
    for item, metric in zip(items, metrics):
        output.append({
            "id_item_tce_ma": item["id_item_tce_ma"],
            "area": item["area"],
            "numero_item": item["numero_item"],
            "texto_original": item["texto_original"],
            "nivel_hierarquico": item["nivel_hierarquico"],
            "item_pai": item["item_pai"],
            "item_folha": item["item_folha"],
            "numero_questoes_correspondencia_direta": len(metric["direta"]),
            "numero_questoes_correspondencia_parcial": len(metric["parcial"]),
            "numero_questoes_apenas_relacionada": len(metric["apenas relacionada"]),
            "numero_total_correspondencias": len(metric["all"]),
            "concursos_distintos": len(metric["contests"]),
            "anos_distintos": len(metric["years"]),
            "ocorrencia_em_questao": len(metric["questions"]),
            "ocorrencia_em_peca_tecnica": len(metric["pieces"]),
            "vinculos_registrados_direta": len(metric["raw_direta"]),
            "vinculos_registrados_parcial": len(metric["raw_parcial"]),
            "vinculos_registrados_apenas_relacionada": len(metric["raw_apenas relacionada"]),
            "vinculos_registrados_total": len(metric["raw_all"]),
            "ids_concursos": json.dumps(sorted(metric["contests"]), ensure_ascii=False),
            "lista_anos": json.dumps(sorted(metric["years"]), ensure_ascii=False),
            "pagina_edital": item["pagina_edital"],
        })
    fields = list(output[0])
    with (ROOT / "dataset/itens_tce_ma_analise.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(output)
    return output


def count_table(counter: Counter[str], total: int, order: list[str] | None = None) -> list[str]:
    keys = order or sorted(counter)
    return [f"| {key} | {counter.get(key, 0)} | {pct(counter.get(key, 0), total)} |" for key in keys]


def top_groups(rows: list[dict[str, str]], limit: int = 4) -> str:
    counts = Counter(group for row in rows for group in thematic_groups(row))
    return "; ".join(f"{name} ({count})" for name, count in counts.most_common(limit)) or "sem agrupamento recorrente"


def main() -> None:
    contests = read_csv("dataset/concursos.csv")
    questions = read_csv("dataset/questoes_discursivas.csv")
    contest_by_id = {row["id_concurso"]: row for row in contests}
    for row in questions:
        row["_categoria"] = contest_by_id[row["id_concurso"]]["categoria_comparabilidade"]
    items = build_items(questions)
    total = len(questions)
    pieces = [row for row in questions if is_piece(row)]
    ordinary = [row for row in questions if not is_piece(row)]

    md: list[str] = [
        "# Análise exploratória descritiva — Fase 3",
        "",
        "> Escopo fechado: os resultados descrevem exclusivamente o corpus de 23 concursos e 56 componentes confirmado nas fases anteriores. Frequência histórica, cobertura e recência nesta amostra não representam probabilidade de cobrança futura.",
        "",
        "## 3.1 — Visão geral",
        "",
        f"O corpus reúne **{len(contests)} concursos**, **{total} componentes discursivos**, dos quais **{len(ordinary)} questões/estudos de caso** e **{len(pieces)} peças técnicas**, no período de **{min(int(r['ano']) for r in questions)} a {max(int(r['ano']) for r in questions)}**.",
        "",
        "### Distribuição por ano",
        "",
        "| Ano | Concursos distintos | Componentes | Percentual dos componentes |",
        "|---:|---:|---:|---:|",
    ]
    for year in sorted({int(r["ano"]) for r in questions}):
        rows = [r for r in questions if int(r["ano"]) == year]
        md.append(f"| {year} | {len({r['id_concurso'] for r in rows})} | {len(rows)} | {pct(len(rows), total)} |")

    md += [
        "",
        "### Distribuição por categoria de órgão",
        "",
        "| Categoria | Concursos | Componentes | Percentual dos componentes |",
        "|---|---:|---:|---:|",
    ]
    for cat in ["A", "B", "C", "D", "E"]:
        cs = [r for r in contests if r["categoria_comparabilidade"] == cat]
        qs = [r for r in questions if r["_categoria"] == cat]
        md.append(f"| {cat} | {len(cs)} | {len(qs)} | {pct(len(qs), total)} |")

    scope_counts = Counter(r["conhecimento_geral_ou_especifico"] for r in questions)
    match_counts = Counter(r["correspondencia_com_edital_tce_ma"] for r in questions)
    md += [
        "",
        "### Conhecimento geral ou específico",
        "",
        "| Natureza | Componentes | Percentual |",
        "|---|---:|---:|",
        *count_table(scope_counts, total, ["geral", "específico"]),
        "",
        "As 13 questões gerais foram mantidas porque integraram a avaliação dos cargos selecionados; elas não foram reclassificadas como técnicas apenas por terem sido aplicadas a candidatos de TI.",
        "",
        "### Correspondência com o edital do TCE-MA",
        "",
        "| Correspondência | Componentes | Percentual |",
        "|---|---:|---:|",
        *count_table(match_counts, total, MATCH_ORDER),
        "",
        "## 3.2 — Cobertura das grandes áreas do Cargo 10",
        "",
        "A classificação é multirrótulo: um componente pode pertencer a mais de uma área. Portanto, as linhas não devem ser somadas como se representassem componentes independentes.",
        "",
        "| Área | Componentes relacionados | Concursos distintos | Anos distintos | Diretas | Parciais | Peças técnicas | Questões não-peça |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for area in AREAS:
        rows = [r for r in questions if area in arr(r, "area_tce_ma")]
        md.append(
            f"| {area} | {len(rows)} | {len({r['id_concurso'] for r in rows})} | {len({r['ano'] for r in rows})} | "
            f"{sum(r['correspondencia_com_edital_tce_ma']=='direta' for r in rows)} | "
            f"{sum(r['correspondencia_com_edital_tce_ma']=='parcial' for r in rows)} | "
            f"{sum(is_piece(r) for r in rows)} | {sum(not is_piece(r) for r in rows)} |"
        )

    direct_items = [i for i in items if i["vinculos_registrados_direta"]]
    partial_only = [i for i in items if i["vinculos_registrados_parcial"] and not i["vinculos_registrados_direta"]]
    related_only = [i for i in items if i["vinculos_registrados_apenas_relacionada"] and not i["vinculos_registrados_direta"] and not i["vinculos_registrados_parcial"]]
    absent_items = [i for i in items if not i["vinculos_registrados_total"]]
    md += [
        "",
        "## 3.3 — Itens do edital",
        "",
        "As métricas principais usam associação canônica no item mais específico disponível. Se uma questão foi vinculada simultaneamente a um pai e a um descendente, o pai preserva o vínculo registrado, mas não recebe uma segunda ocorrência canônica. As listas A–C consideram a existência do vínculo bruto; as colunas de ocorrência, concurso e ano usam somente a associação canônica. Assim se identifica toda a hierarquia sem transformar uma única cobrança em várias ocorrências do mesmo ramo.",
        "",
        f"- **{len(direct_items)} itens** possuem ao menos uma correspondência direta;",
        f"- **{len(partial_only)} itens** possuem correspondência parcial, mas nenhuma direta;",
        f"- **{len(related_only)} itens** aparecem somente como relacionados;",
        f"- **{len(absent_items)} itens** não tiveram correspondência nos 56 componentes analisados.",
        "",
        "### A) Itens com correspondência direta",
        "",
        "| ID | Área | Item | Vínculos diretos | Ocorrências diretas canônicas | Concursos (todas as classes canônicas) | Anos (todas as classes canônicas) |",
        "|---|---|---|---:|---:|---:|---:|",
    ]
    for item in direct_items:
        md.append(f"| {item['id_item_tce_ma']} | {item['area']} | {str(item['texto_original']).replace('|', '\\|')} | {item['vinculos_registrados_direta']} | {item['numero_questoes_correspondencia_direta']} | {item['concursos_distintos']} | {item['anos_distintos']} |")
    md += [
        "",
        "### B) Itens com correspondência apenas parcial (sem direta)",
        "",
        "| ID | Área | Item | Vínculos parciais | Ocorrências parciais canônicas | Concursos (todas as classes canônicas) | Anos (todas as classes canônicas) |",
        "|---|---|---|---:|---:|---:|---:|",
    ]
    for item in partial_only:
        md.append(f"| {item['id_item_tce_ma']} | {item['area']} | {str(item['texto_original']).replace('|', '\\|')} | {item['vinculos_registrados_parcial']} | {item['numero_questoes_correspondencia_parcial']} | {item['concursos_distintos']} | {item['anos_distintos']} |")
    md += [
        "",
        "### Itens somente relacionados",
        "",
        "| ID | Área | Item | Ocorrências relacionadas |",
        "|---|---|---|---:|",
    ]
    for item in related_only:
        md.append(f"| {item['id_item_tce_ma']} | {item['area']} | {str(item['texto_original']).replace('|', '\\|')} | {item['vinculos_registrados_apenas_relacionada']} |")
    md += [
        "",
        "### C) Itens sem correspondência no corpus atual",
        "",
        "Para cada item abaixo, não foi encontrada ocorrência nos 56 componentes analisados. Isso não implica impossibilidade de cobrança.",
        "",
        "| ID | Área | Item | Folha |",
        "|---|---|---|---|",
    ]
    for item in absent_items:
        md.append(f"| {item['id_item_tce_ma']} | {item['area']} | {str(item['texto_original']).replace('|', '\\|')} | {item['item_folha']} |")

    group_rows: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in questions:
        for group in thematic_groups(row):
            group_rows[group].append(row)
    recurrent = {group: rows for group, rows in group_rows.items() if len(rows) >= 2}
    md += [
        "",
        "## 3.4 — Recorrência temática",
        "",
        "Os temas abaixo são agrupamentos analíticos pós-auditoria, não substituem `tema_principal` e aceitam múltiplos rótulos. A tabela separa componentes, concursos e anos para não tratar questões do mesmo certame como observações independentes.",
        "",
        "| Agrupamento temático | Componentes | Concursos distintos | Anos distintos |",
        "|---|---:|---:|---:|",
    ]
    for group, rows in sorted(recurrent.items(), key=lambda x: (-len(x[1]), x[0])):
        md.append(f"| {group} | {len(rows)} | {len({r['id_concurso'] for r in rows})} | {len({r['ano'] for r in rows})} |")

    md += [
        "",
        "## 3.5 — Recência descritiva",
        "",
        "| Período | Componentes | Concursos distintos | Temas mais presentes no período |",
        "|---|---:|---:|---|",
    ]
    for label in ["2015–2018", "2019–2022", "2023–2026"]:
        rows = [r for r in questions if period(int(r["ano"])) == label]
        md.append(f"| {label} | {len(rows)} | {len({r['id_concurso'] for r in rows})} | {top_groups(rows)} |")
    md += [
        "",
        "No período 2015–2018, a amostra combina controle externo, contratações, métodos ágeis/engenharia de software e segurança. Em 2019–2022, o número de componentes é menor e inclui desenvolvimento seguro, segurança organizacional, IA/dados e métodos ágeis. Em 2023–2026, crescem no corpus os registros envolvendo IA/MLOps, dados, cibersegurança, governança e contratações. Essa sequência descreve a composição da amostra e não é usada como inferência de cobrança futura.",
        "",
        "## 3.6 — Forma de cobrança",
        "",
        "As formas também são multirrótulo; seus percentuais usam os 56 componentes como denominador e, por isso, não somam 100%.",
        "",
        "| Forma | Componentes | Percentual |",
        "|---|---:|---:|",
    ]
    form_counts = Counter(form for row in questions for form in arr(row, "forma_cobranca"))
    md.extend(count_table(form_counts, total, FORMS))
    combos = Counter(" + ".join(sorted(map(str, arr(r, "forma_cobranca")), key=lambda x: FORM_ORDER[x])) for r in questions)
    md += [
        "",
        "### Combinações observadas",
        "",
        "| Combinação | Componentes | Percentual |",
        "|---|---:|---:|",
    ]
    for combo, count in combos.most_common():
        md.append(f"| {combo} | {count} | {pct(count, total)} |")

    length_groups = {
        "Questões curtas (até 20 linhas)": [r for r in ordinary if int(r["numero_maximo_linhas"]) <= 20],
        "Questões de 30 linhas": [r for r in ordinary if int(r["numero_maximo_linhas"]) == 30],
        "Outras questões não-peça (>30 linhas)": [r for r in ordinary if int(r["numero_maximo_linhas"]) > 30 and int(r["numero_maximo_linhas"]) != 30],
        "Peças técnicas": pieces,
    }
    md += [
        "",
        "### Forma por extensão/tipo",
        "",
        "| Grupo | N | Conceitual | Situação-problema | Estudo de caso | Análise técnica | Aplicação normativa | Projeto/arquitetura | Peça técnica |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for label, rows in length_groups.items():
        counts = Counter(form for row in rows for form in arr(row, "forma_cobranca"))
        md.append(f"| {label} | {len(rows)} | " + " | ".join(f"{counts[f]} ({pct(counts[f], len(rows))})" for f in FORMS) + " |")

    md += [
        "",
        "## 3.7 — O que o comando exige",
        "",
        "| Característica | Componentes | Percentual |",
        "|---|---:|---:|",
    ]
    for flag in FLAGS:
        count = sum(r[flag] == "sim" for r in questions)
        md.append(f"| `{flag}` | {count} | {pct(count, total)} |")
    md += [
        "",
        "### Questões versus peças técnicas",
        "",
        "| Característica | Questões/estudos (n=47) | Peças (n=9) |",
        "|---|---:|---:|",
    ]
    for flag in FLAGS:
        oq = sum(r[flag] == "sim" for r in ordinary)
        pq = sum(r[flag] == "sim" for r in pieces)
        md.append(f"| `{flag}` | {oq} ({pct(oq, len(ordinary))}) | {pq} ({pct(pq, len(pieces))}) |")
    md += [
        "",
        "### Características por categoria do órgão",
        "",
        "| Categoria | N | Memorização normativa | Aplicação prática | Proposta | Comparação | Explicação conceitual | Cálculo | Código | Diagrama | Legislação |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for cat in ["A", "B", "C"]:
        rows = [r for r in questions if r["_categoria"] == cat]
        values = [sum(r[f] == "sim" for r in rows) for f in FLAGS]
        md.append(f"| {cat} | {len(rows)} | " + " | ".join(f"{n} ({pct(n, len(rows))})" for n in values) + " |")

    md += [
        "",
        "## 3.8 — Peças técnicas",
        "",
        "| Concurso | Ano | Documento | Tema | Situação | Conhecimentos exigidos | Norma/legislação | Linhas | Pontos | Correspondência |",
        "|---|---:|---|---|---|---|---|---:|---:|---|",
    ]
    for row in pieces:
        doc_type = row["tipo_discursiva"].split("—", 1)[-1].strip()
        required = "; ".join(map(str, arr(row, "itens_exigidos")))
        norms = "; ".join(map(str, arr(row, "norma_ou_tecnologia_citada"))) or "nenhuma explicitada"
        cells = [row["id_concurso"], row["ano"], doc_type, row["tema_principal"], row["situacao_problema"], required, norms, row["numero_maximo_linhas"], row["pontuacao"], row["correspondencia_com_edital_tce_ma"]]
        md.append("| " + " | ".join(str(x).replace("|", "\\|").replace("\n", " ") for x in cells) + " |")
    piece_forms = Counter(form for row in pieces for form in arr(row, "forma_cobranca"))
    md += [
        "",
        f"Nas nove peças, **{piece_forms['aplicação normativa']}** usam aplicação normativa, **{piece_forms['estudo de caso']}** foram classificadas como estudo de caso e **{sum(r['exige_proposta_solucao']=='sim' for r in pieces)}** exigem proposta ou medida corretiva. Os documentos solicitados foram pareceres (7), informação (1) e relatório técnico (1). O corpus é pequeno e concentrado em órgãos de controle.",
        "",
        "## 3.9 — Estrutura dos padrões de resposta do CEBRASPE",
        "",
    ]
    topic_counts = [len(arr(r, "itens_exigidos")) for r in questions]
    feature_checks = {
        "definição conceitual": lambda r: bool(re.search(r"\b(defin|conceit)", r["enunciado_integral"], re.I)),
        "justificativa/fundamentação": lambda r: bool(re.search(r"\b(justifi|fundament|esclareça)", r["enunciado_integral"], re.I)),
        "aplicação ao caso": lambda r: r["exige_aplicacao_pratica"] == "sim",
        "exemplos": lambda r: bool(re.search(r"\bexempl", r["enunciado_integral"], re.I)),
        "proposição de medidas": lambda r: r["exige_proposta_solucao"] == "sim",
        "avaliação de conformidade": lambda r: bool(re.search(r"\b(conform|legalidade|de acordo|avalie|avaliando|posicionando-se)", r["enunciado_integral"], re.I)),
    }
    md += [
        f"Os comandos contêm de **{min(topic_counts)} a {max(topic_counts)} tópicos**, com mediana **{statistics.median(topic_counts):g}**. Todos os 56 registros possuem padrão oficial e quesitos armazenados. A rubrica segue os tópicos numerados do comando, mas frequentemente os decompõe em níveis de atendimento ou subelementos.",
        "",
        "| Característica estrutural | Componentes | Percentual |",
        "|---|---:|---:|",
    ]
    for label, check in feature_checks.items():
        count = sum(check(r) for r in questions)
        md.append(f"| {label} | {count} | {pct(count, total)} |")
    explicit_fragments = []
    for row in questions:
        distribution = json.loads(row["distribuicao_pontos_padrao"])
        explicit_fragments.append(len(distribution.get("valores_explicitos_no_enunciado", [])))
    md += [
        "",
        f"A pontuação aparece fragmentada em dois ou mais valores explícitos no comando em **{sum(n >= 2 for n in explicit_fragments)} componentes ({pct(sum(n >= 2 for n in explicit_fragments), total)})**. Nas peças, mesmo quando o comando não explicita cada parcela, os padrões organizam a correção por achados ou blocos. A banca atribui crédito por cobertura graduada dos elementos pedidos, não apenas por uma conclusão global.",
        "",
        "## 3.10 — Diferenças entre tipos de órgão",
        "",
        "| Categoria | Componentes | Geral | Peças | Legislação | Aplicação prática | Direta | Parcial | Relacionada | Inexistente | Temas mais presentes |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for cat in ["A", "B", "C"]:
        rows = [r for r in questions if r["_categoria"] == cat]
        mc = Counter(r["correspondencia_com_edital_tce_ma"] for r in rows)
        md.append(
            f"| {cat} | {len(rows)} | {sum(r['conhecimento_geral_ou_especifico']=='geral' for r in rows)} | {sum(is_piece(r) for r in rows)} | "
            f"{sum(r['exige_conhecimento_legislacao']=='sim' for r in rows)} | {sum(r['exige_aplicacao_pratica']=='sim' for r in rows)} | "
            f"{mc['direta']} | {mc['parcial']} | {mc['apenas relacionada']} | {mc['inexistente']} | {top_groups(rows)} |"
        )
    md += [
        "",
        "A categoria A concentra 46 dos 56 componentes e todas as nove peças técnicas, além da maior parte das questões gerais de controle externo e das aplicações normativas. A categoria B tem seis componentes, com dados/IA e uma avaliação extensa de práticas ágeis e governança. A categoria C tem quatro componentes, concentrados em governança, criptografia, DevSecOps e uma questão geral. As amostras B e C são pequenas; não há concursos D ou E no corpus atual, portanto não há base para uma comparação descritiva dessas categorias.",
        "",
        "## LIMITAÇÕES DO CORPUS",
        "",
        "- A amostra não é aleatória e não representa todo o universo de provas do CEBRASPE.",
        "- Foram incluídos somente concursos localizados e documentalmente confirmados nas fases anteriores.",
        "- Há forte concentração em órgãos de controle e fiscalização (categoria A).",
        "- Os editais e perfis dos cargos diferem entre si, mesmo quando classificados na mesma categoria.",
        "- O período 2015–2026 contém mudanças tecnológicas relevantes; uma mesma denominação pode ter conteúdo histórico distinto.",
        "- Houve mudanças legislativas e de versões de normas; correspondência conceitual não implica identidade normativa.",
        "- Existem apenas nove peças técnicas, todas ligadas a órgãos de controle.",
        "- Questões de um mesmo concurso não são observações independentes.",
        "- Ausência de ocorrência não significa ausência de possibilidade de cobrança.",
        "- A correspondência temática e os agrupamentos recorrentes envolvem julgamento analítico, ainda que documentado e auditado.",
        "- As contagens por área e tema são multirrótulo e não podem ser somadas para obter o total do corpus.",
        "",
        "## Nota de interpretação",
        "",
        "Este relatório apresenta frequências históricas, cobertura do edital atual e diferenças observadas no corpus analisado. Ele não contém ranking preditivo, probabilidade, chance de cobrança ou recomendação de estudo.",
    ]
    (ROOT / "relatorios/analise_exploratoria_fase3.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps({"itens_edital": len(items), "componentes": total, "pecas": len(pieces)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
