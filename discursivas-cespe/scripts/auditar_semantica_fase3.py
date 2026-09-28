#!/usr/bin/env python3
"""Registra a auditoria semântica dos 56 componentes da fase 3.

O script é deliberadamente não destrutivo: ele confronta o CSV corrente com a
decisão de auditoria, mas só grava a trilha de auditoria e o relatório. As
correções do CSV são aplicadas por ``aplicar_correcoes_fase3.py``.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "dataset/questoes_discursivas.csv"
AUDIT_JSON = ROOT / "dados/fase3_auditoria.json"
AUDIT_REPORT = ROOT / "relatorios/auditoria_semantica_fase3.md"

AUDITED_FIELDS = [
    "tema_principal", "subtemas", "conhecimento_geral_ou_especifico",
    "correspondencia_com_edital_tce_ma", "itens_correspondentes_tce_ma",
    "area_tce_ma", "forma_cobranca", "nivel_abstracao",
    "exige_memorizacao_normativa", "exige_aplicacao_pratica",
    "exige_proposta_solucao", "exige_comparacao",
    "exige_explicacao_conceitual", "exige_calculo", "exige_codigo",
    "exige_diagrama", "exige_conhecimento_legislacao", "ano_norma_cobrada",
]

JSON_FIELDS = {
    "subtemas", "itens_correspondentes_tce_ma", "area_tce_ma",
    "forma_cobranca", "ano_norma_cobrada",
}


def correction(reason: str, **changes: object) -> dict[str, object]:
    return {"justificativa": reason, "alteracoes": changes}


# Decisões curadas após leitura conjunta do comando, do padrão oficial e do
# conteúdo programático. Os valores anteriores são obtidos do CSV para que a
# trilha sempre preserve o estado efetivamente auditado.
CORRECTIONS: dict[str, dict[str, object]] = {
    "tce_rj_2021_ace_ti_q1": correction(
        "O comando exige identificar a decisão, expor recursos e delimitar o controle judicial; não solicita comparação entre institutos.",
        exige_comparacao="não",
    ),
    "tce_rj_2021_ace_ti_q3": correction(
        "O conhecimento efetivamente exigido é segurança em BYOD. Arquitetura de soluções mobile e SSO não equivalem, respectivamente, à política BYOD e aos controles de autenticação citados; o texto motivador também não cria um caso concreto a resolver.",
        itens_correspondentes_tce_ma=[
            "GESTÃO E GOVERNANÇA DE TI — 10 Cibersegurança e continuidade de negócios (ISO 27001/22301, 27002, NIST).",
        ],
        area_tce_ma=["GESTÃO E GOVERNANÇA DE TI"],
        forma_cobranca=["conceitual", "análise técnica"],
    ),
    "tce_rj_2021_ace_ti_peca": correction(
        "A peça cobra Lei nº 8.666/1993 e normas históricas do SISP. Há continuidade conceitual com contratações de TI, mas não identidade documental com a Lei nº 14.133/2021 nem com a IN SGD/ME nº 94/2022.",
        itens_correspondentes_tce_ma=[
            "GESTÃO E GOVERNANÇA DE TI — 2 Gestão de riscos de TI (ISO 31000, COSO).",
            "GESTÃO E GOVERNANÇA DE TI — 6 Contratações de TI no setor público.",
            "CONTRATAÇÕES DE TI — 1 Gestão de contratação de soluções de TI.",
            "CONTRATAÇÕES DE TI — 2 Legislação aplicável à contratação de bens e serviços de TI e suas alterações.",
        ],
    ),
    "tcdf_2024_ace_ti_infra_peca": correction(
        "A situação apenas solicita uma informação descritiva sobre as camadas OSI/TCP-IP. Não há solução do problema de rede nem aplicação de norma ao caso; o formato documental deve permanecer identificado como peça técnica.",
        forma_cobranca=["conceitual", "peça técnica"],
        exige_memorizacao_normativa="não",
        exige_aplicacao_pratica="não",
    ),
    "tce_ms_2025_ace_ti_q1": correction(
        "O comando exige apresentar conjuntamente benefícios e limitações da infraestrutura e integração para IA, estabelecendo contraste analítico entre efeitos positivos e restrições.",
        exige_comparacao="sim",
    ),
    "tce_rn_2026_ti_cargo12": correction(
        "Tokens, certificados, biometria e MFA são métodos de autenticação; SSO é mecanismo distinto e não foi exigido. A correspondência parcial subsiste pelo item amplo de cibersegurança.",
        itens_correspondentes_tce_ma=[
            "GESTÃO E GOVERNANÇA DE TI — 10 Cibersegurança e continuidade de negócios (ISO 27001/22301, 27002, NIST).",
        ],
        area_tce_ma=["GESTÃO E GOVERNANÇA DE TI"],
    ),
    "tce_rs_2025_auditor_ti_p3": correction(
        "Competências do TCE/RS e a distinção entre parecer prévio e julgamento decorrem da Constituição e da legislação orgânica; a resposta depende de conteúdo jurídico normativo.",
        forma_cobranca=["conceitual", "aplicação normativa"],
        exige_memorizacao_normativa="sim",
        exige_conhecimento_legislacao="sim",
    ),
    "tce_rs_2025_auditor_ti_p4": correction(
        "A menção à LGPD está no texto declarado unicamente motivador. O comando e a rubrica cobram propriedades de segurança e sua correlação com controles técnicos, sem dispositivo legal, comparação ou edição normativa.",
        itens_correspondentes_tce_ma=[
            "GESTÃO E GOVERNANÇA DE TI — 10 Cibersegurança e continuidade de negócios (ISO 27001/22301, 27002, NIST).",
        ],
        forma_cobranca=["conceitual"],
        exige_memorizacao_normativa="não",
        exige_comparacao="não",
        exige_conhecimento_legislacao="não",
        ano_norma_cobrada=[],
    ),
    "tcdf_2023_ace_sistemas_q2": correction(
        "O cenário apenas motiva uma exposição das práticas de XP, Kanban e Scrum. Os fatos não precisam ser usados para resolver um caso e o comando não contrapõe as metodologias, mas exige recordar elementos definidos dos frameworks.",
        forma_cobranca=["conceitual"],
        exige_memorizacao_normativa="sim",
        exige_aplicacao_pratica="não",
        exige_comparacao="não",
    ),
    "tce_ro_2019_ace_ti_q1": correction(
        "MVP aparece somente no fragmento motivador. A resposta é uma exposição dos controles da ISO/IEC 27002:2013, sem aplicação a fatos específicos; a referência ao projeto de software e à cibersegurança permanece parcial em razão da edição histórica da norma.",
        itens_correspondentes_tce_ma=[
            "ENGENHARIA DE SOFTWARE — 1 Conceitos e técnicas do projeto de software.",
            "GESTÃO E GOVERNANÇA DE TI — 10 Cibersegurança e continuidade de negócios (ISO 27001/22301, 27002, NIST).",
        ],
        forma_cobranca=["conceitual", "aplicação normativa"],
        exige_aplicacao_pratica="não",
    ),
    "tce_mg_2018_ace_cc_q2": correction(
        "Scrum e práticas ágeis estão no edital atual, mas a questão também exige planning poker e todo o modelo GROW, conteúdos relevantes não explicitados; a correspondência é parcial.",
        correspondencia_com_edital_tce_ma="parcial",
    ),
    "cgm_joao_pessoa_2018_auditor_sistemas_q1": correction(
        "Embora o texto contextual mencione validade jurídica da ICP-Brasil, o comando e a rubrica cobram consequências técnicas de certificados, MD5 e DNS e uma solução operacional, sem conhecimento de dispositivo legal.",
        exige_conhecimento_legislacao="não",
    ),
    "tce_pr_2016_analista_informatica_q1": correction(
        "A questão cobra parte expressamente relacionada a projeto e requisitos, mas acrescenta análise econômica, artefatos e diagramas não individualizados no edital; o software hipotético apenas ilustra a exposição, sem fatos que condicionem a resposta.",
        correspondencia_com_edital_tce_ma="parcial",
        forma_cobranca=["conceitual"],
        exige_aplicacao_pratica="não",
    ),
    "tce_pr_2016_analista_informatica_peca": correction(
        "O parecer não apenas avalia: o comando exige complementar lacunas e a rubrica demanda sugerir proposição adequada quando a proposição auditada estiver errada.",
        exige_proposta_solucao="sim",
    ),
    "tcu_2015_aufc_ti_p3_q1": correction(
        "O núcleo do comando é equilibrar confidencialidade e transparência e tratar os limites entre esses deveres, o que exige contraposição explícita.",
        exige_comparacao="sim",
    ),
    "sefaz_ce_2021_auditor_ti_q2": correction(
        "Solicitar a descrição de dois tipos de redes neurais não equivale a exigir que sejam comparados; a rubrica pontua citação e descrição separadas.",
        exige_comparacao="não",
    ),
    "sefaz_ce_2021_auditor_ti_estudo": correction(
        "Para os achados rejeitados, o comando exige sugerir proposições de melhoria apropriadas e a rubrica pontua expressamente essa proposta.",
        exige_proposta_solucao="sim",
    ),
    "trt10_2025_analista_ti_q1": correction(
        "O texto motivador não configura caso concreto. O comando pede pressupostos, objetivos e benefícios de DevSecOps/OWASP SAMM, sem aplicar os conceitos a uma organização específica.",
        exige_aplicacao_pratica="não",
    ),
}


def read_rows() -> list[dict[str, str]]:
    with QUESTIONS.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def typed_value(field: str, value: str) -> object:
    return json.loads(value) if field in JSON_FIELDS else value


def generic_match_reason(row: dict[str, str], final: dict[str, object]) -> str:
    match = str(final["correspondencia_com_edital_tce_ma"])
    theme = str(final["tema_principal"])
    items = final["itens_correspondentes_tce_ma"]
    if match == "direta":
        return f"O conceito efetivamente exigido em “{theme}” encontra cobertura expressa ou inequivocamente equivalente nos itens registrados do edital."
    if match == "parcial":
        return f"Há cobertura substancial de “{theme}”, mas a questão também exige tecnologia, norma, versão ou detalhe relevante não explicitado no edital atual."
    if match == "apenas relacionada":
        return f"Os itens registrados pertencem a domínio próximo de “{theme}”, porém não cobrem diretamente o conhecimento específico exigido."
    return f"Não foi identificado item do edital do TCE-MA que cubra adequadamente o conhecimento exigido em “{theme}”."


def main() -> None:
    rows = read_rows()
    if len(rows) != 56:
        raise SystemExit(f"Esperados 56 componentes, encontrados {len(rows)}")
    ids = {row["id_questao"] for row in rows}
    unknown = sorted(set(CORRECTIONS) - ids)
    if unknown:
        raise SystemExit(f"Correções referenciam IDs ausentes: {unknown}")

    components: list[dict[str, object]] = []
    changes_total = 0
    components_changed = 0
    states = Counter()

    for row in rows:
        spec = CORRECTIONS.get(row["id_questao"], {"justificativa": "", "alteracoes": {}})
        proposed = dict(spec["alteracoes"])
        before = {field: typed_value(field, row[field]) for field in AUDITED_FIELDS}
        final = dict(before)
        final.update(proposed)
        changes = []
        for field, new in proposed.items():
            old = before[field]
            if old == new:
                state = "já corrigida no CSV"
            else:
                state = "pendente no CSV"
                changes_total += 1
            changes.append({
                "campo": field,
                "valor_anterior": old,
                "valor_corrigido": new,
                "justificativa": spec["justificativa"],
                "documentos_fundamentadores": [
                    row["fonte_enunciado"], row["fonte_padrao_resposta"],
                    "dados/tce_ma_conteudo_programatico.json",
                ],
                "estado": state,
            })
        if changes:
            components_changed += 1
        current_matches_final = all(typed_value(field, row[field]) == final[field] for field in AUDITED_FIELDS)
        states["aplicada" if current_matches_final else "pendente"] += 1
        components.append({
            "id_questao": row["id_questao"],
            "id_concurso": row["id_concurso"],
            "ano": int(row["ano"]),
            "tipo_discursiva": row["tipo_discursiva"],
            "fontes_confrontadas": {
                "enunciado": row["fonte_enunciado"],
                "padrao_resposta": row["fonte_padrao_resposta"],
                "edital_tce_ma": "dados/tce_ma_conteudo_programatico.json",
            },
            "presenca_textual": {
                "enunciado_integral": bool(row["enunciado_integral"].strip()),
                "padrao_resposta": bool(row["texto_padrao_resposta"].strip()),
                "quesitos_avaliados": bool(row["quesitos_avaliados"].strip()),
            },
            "campos_auditados_valor_anterior": before,
            "campos_auditados_valor_final": final,
            "justificativa_tematica": (
                f"Tema e subtemas foram confrontados com o comando integral e com a rubrica oficial; “{final['tema_principal']}” sintetiza o núcleo efetivamente pontuado sem substituir o texto primário."
            ),
            "justificativa_correspondencia": generic_match_reason(row, final),
            "alteracoes": changes,
            "resultado": "corrigida" if changes else "mantida",
            "estado_no_csv": "final" if current_matches_final else "pré-correção",
        })

    report_state = "aplicadas" if states["pendente"] == 0 else "registradas antes da aplicação"
    audit = {
        "fase": 3,
        "data_auditoria": date.today().isoformat(),
        "escopo": {
            "concursos": 23,
            "componentes_discursivos": 56,
            "pecas_tecnicas": 9,
            "novos_concursos_incorporados": 0,
        },
        "metodo": {
            "ordem": "enunciado integral → padrão de resposta/quesitos → tema e forma → correspondência conceitual com o edital",
            "unidade": "componente discursivo",
            "campos_auditados": AUDITED_FIELDS,
            "regra_normas_historicas": "preservar a norma histórica e distinguir continuidade conceitual de identidade de norma/versão",
            "regra_geral_especifico": "natureza do componente aplicado ao cargo, mantendo componentes comuns/gerais no corpus",
        },
        "resultado": {
            "status": report_state,
            "componentes_auditados": len(components),
            "componentes_com_correcao": components_changed,
            "classificacoes_corrigidas": sum(len(c["alteracoes"]) for c in components),
            "alteracoes_ainda_pendentes_no_csv": changes_total,
        },
        "componentes": components,
    }
    AUDIT_JSON.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = [
        "# Auditoria semântica — Fase 3",
        "",
        "## Status",
        "",
        f"Foram auditados **{len(components)} de 56 componentes**. As decisões de correção estão **{report_state}**. A auditoria registrou **{sum(len(c['alteracoes']) for c in components)} correções de campos analíticos em {components_changed} componentes**.",
        "",
        "Nenhum enunciado, padrão de resposta, URL ou identificador documental integra a lista de campos alteráveis desta auditoria. Não houve pesquisa, download ou incorporação de concurso.",
        "",
        "## Método e critérios",
        "",
        "Cada registro foi lido na ordem: enunciado integral; padrão e quesitos oficiais; classificação temática e forma de cobrança; itens do conteúdo programático. A correspondência foi julgada pelo conceito efetivamente pontuado, não por palavras isoladas. Menções em trechos declarados unicamente motivadores não foram tratadas automaticamente como conteúdo exigido.",
        "",
        "Normas históricas foram preservadas. Quando o processo permanece no edital, mas a norma ou versão mudou, a relação foi mantida como parcial e a identidade com o ato atual foi removida. `exige_conhecimento_legislacao` foi reservado a conhecimento jurídico efetivamente necessário; normas técnicas e frameworks permanecem separados em `exige_memorizacao_normativa`.",
        "",
        "## Correções registradas",
        "",
        "| Componente | Campo | Valor anterior | Valor corrigido | Fundamento resumido |",
        "|---|---|---|---|---|",
    ]
    for component in components:
        for change in component["alteracoes"]:
            old = json.dumps(change["valor_anterior"], ensure_ascii=False) if isinstance(change["valor_anterior"], (list, dict)) else str(change["valor_anterior"])
            new = json.dumps(change["valor_corrigido"], ensure_ascii=False) if isinstance(change["valor_corrigido"], (list, dict)) else str(change["valor_corrigido"])
            reason = str(change["justificativa"])
            md.append(f"| `{component['id_questao']}` | `{change['campo']}` | {old.replace('|', '\\|')} | {new.replace('|', '\\|')} | {reason.replace('|', '\\|')} |")
    md += [
        "",
        "## Cobertura integral da auditoria",
        "",
        "A tabela abaixo explicita os 56 componentes confrontados. “Mantida” significa que todos os 18 campos auditados permaneceram semanticamente adequados; “corrigida” indica ao menos uma mudança documentada acima.",
        "",
        "| # | Componente | Concurso | Ano | Tipo | Resultado | Estado no CSV | Correspondência final | Tema final |",
        "|---:|---|---|---:|---|---|---|---|---|",
    ]
    for number, component in enumerate(components, 1):
        final = component["campos_auditados_valor_final"]
        md.append(
            f"| {number} | `{component['id_questao']}` | `{component['id_concurso']}` | {component['ano']} | {component['tipo_discursiva']} | {component['resultado']} | {component['estado_no_csv']} | {final['correspondencia_com_edital_tce_ma']} | {str(final['tema_principal']).replace('|', '\\|')} |"
        )
    md += [
        "",
        "## Problemas semânticos encontrados",
        "",
        "- associação de mecanismos apenas próximos, como SSO e MFA, sem equivalência conceitual;",
        "- uso de itens específicos da legislação atual para questões regidas por normas históricas;",
        "- transformação de textos apenas motivadores em situação-problema ou em exigência legal;",
        "- marcação de comparação quando o comando somente solicitava descrições independentes;",
        "- ausência de marcação de proposta quando a rubrica pontuava uma solução corretiva;",
        "- superestimação de aplicação prática em questões puramente expositivas.",
        "",
        "## Rastreabilidade",
        "",
        "A justificativa completa, os valores anterior e final de todos os campos, e as referências documentais de cada um dos 56 componentes estão em `dados/fase3_auditoria.json`.",
    ]
    AUDIT_REPORT.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps(audit["resultado"], ensure_ascii=False))


if __name__ == "__main__":
    main()
