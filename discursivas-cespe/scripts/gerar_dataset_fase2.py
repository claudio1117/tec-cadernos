#!/usr/bin/env python3
"""Consolida a fase 2 sem alterar os valores dos registros validados na fase 1.

Os textos primarios sao extraidos dos PDFs locais oficiais. A normalizacao feita
remove apenas artefatos de leiaute e espacos; nao resume enunciados nem padroes.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "dados/fase2_fontes.json").read_text(encoding="utf-8"))
EDITAL_TCE = json.loads((ROOT / "dados/tce_ma_conteudo_programatico.json").read_text(encoding="utf-8"))


def jlist(*items: object) -> str:
    return json.dumps(list(items), ensure_ascii=False)


def load_phase1() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    path = ROOT / "scripts/gerar_dataset_validacao.py"
    spec = importlib.util.spec_from_file_location("fase1", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Nao foi possivel carregar o gerador da fase 1")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return [dict(row) for row in module.CONCURSOS], [dict(row) for row in module.build_questions()]


def manifest_event(event: str) -> dict[str, object]:
    matches = [row for row in MANIFEST if row["identificador_api"] == event]
    if len(matches) != 1:
        raise RuntimeError(f"Evento ausente ou duplicado no manifesto: {event}")
    return matches[0]


def doc(event: str, local_name: str) -> dict[str, object]:
    row = manifest_event(event)
    matches = [d for d in row["documentos"] if Path(d["arquivo_local"]).name == local_name]
    if len(matches) != 1:
        raise RuntimeError(f"Documento ausente ou duplicado: {event}/{local_name}")
    return matches[0]


def urls(event: str, kind: str) -> str:
    values = [d["url"] for d in manifest_event(event)["documentos"] if d["tipo"] == kind]
    return values[0] if len(values) == 1 else json.dumps(values, ensure_ascii=False)


def decode_tcesc_font(text: str) -> str:
    # O PDF oficial de 2021 usa uma codificacao de glifos deslocada. A tabela
    # abaixo apenas reverte o mapa ToUnicode defeituoso do proprio documento.
    accents = {"m": "ã", "o": "ç", "p": "é", "t": "í", "y": "ó", "i": "á",
               "}": "õ", "r": "ê", "j": "à", "~": "ú", "q": "è", "v": "ì",
               "z": "ò", "{": "ô", "k": "â", "e": "É"}
    out: list[str] = []
    for char in text:
        code = ord(char)
        if char in "\n\r\t\f":
            out.append(char)
        elif char in accents:
            out.append(accents[char])
        elif 0x03 <= code <= 0x1F:
            out.append(chr(code + 29))
        elif "$" <= char <= "=":
            out.append(chr(code + 29))
        elif "D" <= char <= "Z" or char in "[\\]^_`abc":
            out.append(chr(code - 3).lower())
        elif char == ">":
            out.append("[")
        elif char == "@":
            out.append("]")
        elif char == "\x90":
            out.append("-")
        else:
            out.append(char)
    return "".join(out)


def pdf_text(local_path: str, pages: tuple[int, ...], decode_tcesc: bool = False) -> str:
    path = ROOT / local_path
    pieces: list[str] = []
    for page in pages:
        result = subprocess.run(
            ["pdftotext", "-layout", "-f", str(page), "-l", str(page), str(path), "-"],
            check=True, capture_output=True, text=True, errors="replace",
        )
        pieces.append(result.stdout)
    text = "\n".join(pieces)
    if decode_tcesc:
        text = decode_tcesc_font(text)
    text = text.replace("\f", "\n").replace("\x00", " ").replace("\x03", " ")
    lines = []
    for line in text.splitlines():
        compact = re.sub(r"\s+", " ", line).strip()
        if not compact:
            continue
        if re.search(r"(?:CESPE\s*\|\s*)?CEBRASPE\s*[–|\\]", compact, re.I):
            continue
        if re.fullmatch(r"Cargo:\s*(?:–\d+–)?", compact):
            continue
        lines.append(compact)
    return "\n".join(lines).strip()


def excerpt(text: str, start: str, end: str | None = "RASCUNHO") -> str:
    pos = text.find(start)
    if pos < 0:
        raise RuntimeError(f"Marcador inicial nao localizado: {start!r}")
    text = text[pos:]
    if end:
        finish = text.find(end)
        if finish >= 0:
            text = text[:finish]
    return re.sub(r"\s+", " ", text).strip()


def mapped(*indices: int) -> str:
    values = []
    for index in indices:
        item = EDITAL_TCE[index]
        values.append(f"{item['area']} — {item['texto_original_edital']}")
    return jlist(*values)


CONTEST_SPECS = [
    ("TCE_RN_25", "tce_rn_2026_ti", 2026, "Tribunal de Contas do Estado do Rio Grande do Norte (TCE/RN)", "Analista Administrativo; Auditor de Controle Externo", "Tecnologia da Informação — cargos 4, 5 e 12", "Tribunal de Contas estadual", "A", "Provas aplicadas em 11/4/2026 (cargo 12) e 12/4/2026 (cargos 4 e 5)."),
    ("TCE_MG_25", "tce_mg_2026_ace_cc", 2026, "Tribunal de Contas do Estado de Minas Gerais (TCE/MG)", "Analista de Controle Externo", "Ciência da Computação — cargo 1", "Tribunal de Contas estadual", "A", "Edital 2025; prova aplicada em 25/1/2026."),
    ("TCE_RS_25", "tce_rs_2025_auditor_ti", 2025, "Tribunal de Contas do Estado do Rio Grande do Sul (TCE/RS)", "Auditor de Controle Externo", "Tecnologia da Informação — cargo 4", "Tribunal de Contas estadual", "A", "Provas P3 e P4 aplicadas em 19/10/2025."),
    ("TCE_PR_24_AUDITOR", "tce_pr_2024_auditor_informatica", 2024, "Tribunal de Contas do Estado do Paraná (TCE/PR)", "Auditor de Controle Externo", "Informática — cargo 5", "Tribunal de Contas estadual", "A", "Provas aplicadas em 10/8/2024."),
    ("TCE_AC_24", "tce_ac_2024_analista_ti", 2024, "Tribunal de Contas do Estado do Acre (TCE/AC)", "Analista de Tecnologia da Informação", "Gestão de Dados; Infraestrutura de TI; Planejamento de TI; Projetos de TI; Segurança da Informação; Sistemas de Informação — cargos 6 a 11", "Tribunal de Contas estadual", "A", "Discursiva comum aos cargos superiores 1 a 13, aplicada em 1/9/2024; registrada uma vez para evitar duplicação artificial."),
    ("TC_DF_23", "tcdf_2023_ace_sistemas", 2023, "Tribunal de Contas do Distrito Federal (TCDF)", "Auditor de Controle Externo – Área Especializada", "Tecnologia da Informação – Orientação Sistemas de TI — cargo 3", "Tribunal de Contas distrital", "A", "Prova aplicada em 17/12/2023; certame distinto do TCDF 2024 da fase 1."),
    ("TCE_SC_21_AUDITOR", "tce_sc_2022_auditor_cc", 2022, "Tribunal de Contas do Estado de Santa Catarina (TCE/SC)", "Auditor Fiscal de Controle Externo", "Ciências da Computação — cargo 3", "Tribunal de Contas estadual", "A", "Edital 2021; prova aplicada em 6/3/2022. O mapa de caracteres do PDF exigiu reversão documental, sem alteração do conteúdo."),
    ("TCE_RO_19", "tce_ro_2019_ace_ti", 2019, "Tribunal de Contas do Estado de Rondônia (TCE/RO)", "Auditor de Controle Externo", "Tecnologia da Informação — cargo 1", "Tribunal de Contas estadual", "A", "Prova aplicada em 20/10/2019."),
    ("TCE_MG_18", "tce_mg_2018_ace_cc", 2018, "Tribunal de Contas do Estado de Minas Gerais (TCE/MG)", "Analista de Controle Externo", "Ciências da Computação — cargo 4", "Tribunal de Contas estadual", "A", "Prova aplicada em 2018."),
    ("PREF_JP_17_CGM", "cgm_joao_pessoa_2018_auditor_sistemas", 2018, "Controladoria-Geral do Município de João Pessoa (CGM/JP)", "Auditor Municipal de Controle Interno", "Desenvolvimento de Sistemas — cargo 3", "Controladoria municipal", "A", "Edital 2017; prova aplicada em 28/1/2018."),
    ("TCE_PR_16_ANALISTA", "tce_pr_2016_analista_informatica", 2016, "Tribunal de Contas do Estado do Paraná (TCE/PR)", "Analista de Controle", "Informática — cargo 8", "Tribunal de Contas estadual", "A", "Provas aplicadas em 11/9/2016. A API oficial disponibiliza apenas padrões preliminares para os cinco componentes."),
    ("TCE_PA_16", "tce_pa_2016_auditor_informatica", 2016, "Tribunal de Contas do Estado do Pará (TCE/PA)", "Auditor de Controle Externo", "Informática — cargos 32 a 36", "Tribunal de Contas estadual", "A", "Discursiva geral comum aos cargos 1 e 18 a 38, aplicada em 7/8/2016; registrada uma vez para as cinco especialidades de TI."),
    ("TCU_15_AUFC", "tcu_2015_aufc_ti", 2015, "Tribunal de Contas da União (TCU)", "Auditor Federal de Controle Externo", "Tecnologia da Informação — cargo 2", "Tribunal de Contas da União", "A", "Provas P3 e P4 aplicadas em 16/8/2015."),
    ("TCU_25_AUFC", "tcu_2026_aufc_auditoria_ti", 2026, "Tribunal de Contas da União (TCU)", "Auditor Federal de Controle Externo – Área Controle Externo", "Orientação: Auditoria de Tecnologia da Informação", "Tribunal de Contas da União", "A", "Edital 2025; prova aplicada em 22/2/2026. Incorporado antes da análise temática, substituindo o CNJ 2024 por prioridade/comparabilidade superiores."),
    ("SEFAZ_SE_25_AUDITOR", "sefaz_se_2025_auditor_ti", 2025, "Secretaria de Estado da Fazenda de Sergipe (SEFAZ/SE)", "Auditor Fiscal Tributário", "Tecnologia da Informação — especialidade 2", "Secretaria de Fazenda estadual", "B", "Prova aplicada em 28/9/2025."),
    ("SEFA_PR_25", "sefa_pr_2026_agente_ti", 2026, "Secretaria de Estado da Fazenda do Paraná (SEFA/PR)", "Agente Fazendário Estadual", "Profissional de Tecnologia da Informação — cargo 6", "Secretaria de Fazenda estadual", "B", "Edital 2025; prova comum aos cargos 1 a 6, aplicada em 25/1/2026."),
    ("SEFAZ_CE_21", "sefaz_ce_2021_auditor_ti", 2021, "Secretaria da Fazenda do Estado do Ceará (SEFAZ/CE)", "Auditor Fiscal", "Tecnologia da Informação da Receita Estadual — cargo 4", "Secretaria de Fazenda estadual", "B", "Prova aplicada em 15/8/2021."),
    ("STJ_24", "stj_2024_analista_ti", 2024, "Superior Tribunal de Justiça (STJ)", "Analista Judiciário – Área Apoio Especializado", "Análise de Sistemas de Informação — cargo 3; Suporte em Tecnologia da Informação — cargo 18", "Poder Judiciário", "C", "Provas específicas por especialidade, aplicadas em 1/12/2024."),
    ("TRT10_24", "trt10_2025_analista_ti", 2025, "Tribunal Regional do Trabalho da 10.ª Região (TRT10)", "Analista Judiciário – Área Apoio Especializado", "Tecnologia da Informação — cargo 11", "Poder Judiciário", "C", "Edital 2024; prova aplicada em 16/3/2025."),
    ("TRF6_24", "trf6_2025_analistas_ti", 2025, "Tribunal Regional Federal da 6.ª Região (TRF6)", "Analista Judiciário – Área Apoio Especializado", "Análise de Dados; Análise de Sistemas de Informação; Governança e Gestão de TI; Tecnologia da Informação — cargos 2, 3, 13 e 22", "Poder Judiciário", "C", "Edital 2024; discursiva geral comum aos cargos superiores indicados, aplicada em 19/1/2025 e registrada uma vez."),
]


def build_contests() -> tuple[list[dict[str, object]], dict[str, dict[str, object]]]:
    rows = []
    by_id = {}
    for event, cid, year, org, cargo, specialty, org_type, category, notes in CONTEST_SPECS:
        row = {
            "id_concurso": cid, "ano": year, "orgao": org, "cargo": cargo,
            "especialidade": specialty, "banca": "CEBRASPE", "tipo_orgao": org_type,
            "nivel_cargo": "superior", "categoria_comparabilidade": category,
            "url_edital": urls(event, "editais"), "url_prova": urls(event, "provas"),
            "url_padrao_resposta": urls(event, "padroes_resposta"),
            "fonte_oficial": "sim — apis.cebraspe.org.br e cdn.cebraspe.org.br",
            "status_confirmacao": "confirmado", "observacoes": notes + f" Evento oficial: {event}.",
        }
        rows.append(row)
        by_id[cid] = row
    return rows, by_id


def qspec(qid: str, cid: str, proof: str, proof_pages: tuple[int, ...], start: str,
          pattern: str, pattern_pages: tuple[int, ...], *, kind: str, lines: int,
          points: str, required: tuple[str, ...], theme: str, subthemes: tuple[str, ...],
          situation: str, citations: tuple[str, ...], scope: str, match: str,
          item_indices: tuple[int, ...], area: tuple[str, ...], form: tuple[str, ...],
          abstraction: str = "médio", normative: str = "não", practical: str = "não",
          solution: str = "não", comparison: str = "não", conceptual: str = "sim",
          calculation: str = "não", code: str = "não", diagram: str = "não",
          legislation: str = "não", norm_years: tuple[int, ...] = (),
          end: str | None = "RASCUNHO", decode_tcesc: bool = False,
          notes: str = "", exact_cargo: str | None = None,
          exact_specialty: str | None = None) -> dict[str, object]:
    return locals()


Q_SPECS = [
    qspec("tce_rn_2026_ti_cargo4", "tce_rn_2026_ti", "tce_rn_2026_cargo4_discursiva.pdf", (1,), "A modelagem de dados",
          "tce_rn_2026_cargo4_padrao_definitivo.pdf", (1, 2), kind="questão dissertativa", lines=30, points="20,00",
          required=("características e finalidades dos modelos conceitual, lógico e físico", "contribuição da modelagem para integridade e redução de inconsistências", "modelagem física e otimização por índices, particionamento e armazenamento"),
          theme="Modelagem de dados conceitual, lógica e física", subthemes=("integridade", "índices", "particionamento", "armazenamento", "desempenho"),
          situation="Exposição técnica sobre modelos de dados e seus efeitos na implementação.", citations=("modelagem conceitual", "modelagem lógica", "modelagem física"), scope="específico", match="direta", item_indices=(8, 11, 14, 19, 21, 22),
          area=("ENGENHARIA DE DADOS",), form=("conceitual", "análise técnica"), comparison="sim", exact_cargo="Analista Administrativo", exact_specialty="Tecnologia da Informação (Desenvolvimento de Sistemas e Inteligência da Informação) — cargo 4"),
    qspec("tce_rn_2026_ti_cargo5", "tce_rn_2026_ti", "tce_rn_2026_cargo5_discursiva.pdf", (1,), "Uma empresa possui",
          "tce_rn_2026_cargo5_padrao_definitivo.pdf", (1,), kind="questão dissertativa", lines=30, points="20,00",
          required=("organização da rede e acesso à aplicação", "segurança e monitoramento da rede e dos servidores web", "backup e disponibilidade da aplicação"),
          theme="Infraestrutura, segurança e continuidade de aplicação web", subthemes=("segmentação de rede", "monitoramento", "servidores web", "backup", "alta disponibilidade"),
          situation="Aplicação local crítica com indisponibilidade, lentidão, acessos indevidos e falhas de backup.", citations=("segmentação de rede", "backup"), scope="específico", match="parcial", item_indices=(87, 100),
          area=("ARQUITETURA DE SOFTWARE", "GESTÃO E GOVERNANÇA DE TI"), form=("situação-problema", "projeto/arquitetura"), practical="sim", solution="sim", conceptual="não", exact_cargo="Analista Administrativo", exact_specialty="Tecnologia da Informação (Infraestrutura, Segurança e Suporte) — cargo 5",
          notes="Correspondência parcial: redes e rotinas de backup não estão detalhadas no edital, embora arquitetura web, cibersegurança e continuidade estejam presentes."),
    qspec("tce_rn_2026_ti_cargo12", "tce_rn_2026_ti", "tce_rn_2026_cargo12_discursiva.pdf", (1,), "Estudo de caso",
          "tce_rn_2026_cargo12_padrao_definitivo.pdf", (1, 2), kind="estudo de caso", lines=45, points="30,00",
          required=("tokens, certificados digitais e biometria: características, vantagens e limitações", "riscos do uso exclusivo de senhas", "importância de MFA e autenticação robusta"),
          theme="Métodos de autenticação e controle de acesso", subthemes=("senhas", "tokens", "certificados digitais", "biometria", "MFA", "identidade"),
          situation="Auditoria encontra credenciais comprometidas e adulteração de dados em sistema de prestação de contas.", citations=("MFA", "certificados digitais", "tokens", "biometria"), scope="específico", match="parcial", item_indices=(90, 100),
          area=("ARQUITETURA DE SOFTWARE", "GESTÃO E GOVERNANÇA DE TI"), form=("estudo de caso", "análise técnica"), practical="sim", comparison="sim", exact_cargo="Auditor de Controle Externo", exact_specialty="Tecnologia da Informação — cargo 12",
          notes="Correspondência parcial: o edital cobre cibersegurança e autenticação única, mas não enumera os métodos cobrados."),

    qspec("tce_mg_2026_ace_cc_q1", "tce_mg_2026_ace_cc", "tce_mg_2025_cargo1_discursiva.pdf", (1,), "Questão 1",
          "tce_mg_2025_cargo1_padrao_definitivo.pdf", (1, 2), kind="questão dissertativa", lines=60, points="10,00",
          required=("modalidades de controle", "objetos da fiscalização", "apreciação e julgamento de contas", "tomada de contas especial"),
          theme="Controle da administração pública em Minas Gerais", subthemes=("controle externo", "fiscalização", "contas de governo", "contas de gestão", "tomada de contas especial"),
          situation="Exposição normativa sobre o sistema de controle estadual.", citations=("Constituição do Estado de Minas Gerais", "Lei Complementar estadual n.º 102/2008"), scope="geral", match="inexistente", item_indices=(), area=(), form=("aplicação normativa", "conceitual"), normative="sim", legislation="sim", norm_years=(2008,)),
    qspec("tce_mg_2026_ace_cc_q2", "tce_mg_2026_ace_cc", "tce_mg_2025_cargo1_discursiva.pdf", (4,), "Questão 2",
          "tce_mg_2025_cargo1_padrao_definitivo.pdf", (3, 4), kind="questão dissertativa", lines=60, points="10,00",
          required=("diferenças entre ETL e ELT", "transferência de arquivos e integração via base de dados", "proposta de fluxo para fontes heterogêneas"),
          theme="Técnicas de integração e ingestão de dados", subthemes=("ETL", "ELT", "transferência de arquivos", "integração via banco", "integridade", "escalabilidade"),
          situation="Escolha de técnicas para integrar múltiplas fontes heterogêneas.", citations=("ETL", "ELT"), scope="específico", match="direta", item_indices=(3, 23), area=("ENGENHARIA DE DADOS",),
          form=("conceitual", "análise técnica", "projeto/arquitetura"), practical="sim", solution="sim", comparison="sim"),

    qspec("tce_rs_2025_auditor_ti_p3", "tce_rs_2025_auditor_ti", "tce_rs_2025_p3_geral_discursiva.pdf", (1,), "No ciclo das finanças públicas",
          "tce_rs_2025_p3_geral_padrao_definitivo.pdf", (1, 2), kind="questão dissertativa", lines=15, points="20,00",
          required=("competências do TCE/RS e interface com a Assembleia Legislativa", "distinção entre parecer prévio e julgamento de contas"),
          theme="Competências do TCE/RS no controle externo", subthemes=("contas de governo", "contas de gestão", "parecer prévio"),
          situation="Exposição sobre controle externo no ciclo das finanças públicas.", citations=("TCE/RS",), scope="geral", match="inexistente", item_indices=(), area=(), form=("conceitual",), comparison="sim"),
    qspec("tce_rs_2025_auditor_ti_p4", "tce_rs_2025_auditor_ti", "tce_rs_2025_cargo4_p4_discursiva.pdf", (1,), "Órgãos de controle geralmente",
          "tce_rs_2025_cargo4_p4_padrao_definitivo.pdf", (1, 2), kind="questão dissertativa", lines=15, points="20,00",
          required=("propriedades da segurança da informação", "correlação de criptografia, assinatura digital e MFA com as propriedades"),
          theme="Propriedades e controles de segurança da informação", subthemes=("confidencialidade", "integridade", "disponibilidade", "autenticidade", "não repúdio", "criptografia", "assinatura digital", "MFA"),
          situation="Proteção de processos eletrônicos e dados pessoais em órgãos de controle.", citations=("LGPD", "criptografia", "assinatura digital", "MFA"), scope="específico", match="direta", item_indices=(100, 102),
          area=("GESTÃO E GOVERNANÇA DE TI",), form=("conceitual", "aplicação normativa"), comparison="sim", normative="sim", legislation="sim", norm_years=(2018,)),

    qspec("tce_pr_2024_auditor_informatica_q1", "tce_pr_2024_auditor_informatica", "tce_pr_2024_cargo5_discursiva.pdf", (1,), "QUESTÃO 1",
          "tce_pr_2024_cargo5_padrao_definitivo.pdf", (1, 2), kind="questão dissertativa", lines=15, points="5,00",
          required=("tamanho de endereços IPv4 e IPv6", "nomenclatura", "tipos de endereçamento de pacotes"), theme="Endereçamento IPv4 e IPv6", subthemes=("TCP/IP", "IPv4", "IPv6", "unicast", "multicast", "broadcast", "anycast"),
          situation="Comparação técnica dos protocolos de endereçamento.", citations=("TCP/IP", "IPv4", "IPv6"), scope="específico", match="inexistente", item_indices=(), area=(), form=("conceitual",), comparison="sim"),
    qspec("tce_pr_2024_auditor_informatica_q2", "tce_pr_2024_auditor_informatica", "tce_pr_2024_cargo5_discursiva.pdf", (2,), "QUESTÃO 2",
          "tce_pr_2024_cargo5_padrao_definitivo.pdf", (3,), kind="questão dissertativa", lines=15, points="5,00",
          required=("processamento em lote", "processamento em tempo real", "situação indicada para cada modalidade"), theme="Processamento de dados em lote e em tempo real", subthemes=("batch", "tempo real"),
          situation="Comparação de modalidades de processamento de dados.", citations=("processamento em lote", "processamento em tempo real"), scope="específico", match="apenas relacionada", item_indices=(0, 3), area=("ENGENHARIA DE DADOS",), form=("conceitual",), comparison="sim"),
    qspec("tce_pr_2024_auditor_informatica_q3", "tce_pr_2024_auditor_informatica", "tce_pr_2024_cargo5_discursiva.pdf", (3,), "QUESTÃO 3",
          "tce_pr_2024_cargo5_padrao_definitivo.pdf", (4, 5), kind="questão dissertativa", lines=15, points="5,00",
          required=("acerto da decisão do TCE", "natureza jurídica das contas do presidente da assembleia"), theme="Julgamento de contas do chefe do Poder Legislativo", subthemes=("tribunal de contas", "contas de gestão", "sanções"),
          situation="Presidente de assembleia recorre de contas julgadas irregulares.", citations=("jurisprudência do STF",), scope="geral", match="inexistente", item_indices=(), area=(), form=("situação-problema", "aplicação normativa"), normative="sim", practical="sim", legislation="sim"),
    qspec("tce_pr_2024_auditor_informatica_q4", "tce_pr_2024_auditor_informatica", "tce_pr_2024_cargo5_discursiva.pdf", (4,), "QUESTÃO 4",
          "tce_pr_2024_cargo5_padrao_definitivo.pdf", (6,), kind="questão dissertativa", lines=15, points="5,00",
          required=("definição de risco de auditoria", "resposta do auditor aos riscos avaliados"), theme="Risco de auditoria", subthemes=("distorção relevante", "resposta do auditor"), situation="Exposição conceitual de auditoria.", citations=("risco de auditoria",), scope="geral", match="inexistente", item_indices=(), area=(), form=("conceitual", "aplicação normativa"), normative="sim"),
    qspec("tce_pr_2024_auditor_informatica_peca", "tce_pr_2024_auditor_informatica", "tce_pr_2024_cargo5_discursiva.pdf", (5,), "PARECER",
          "tce_pr_2024_cargo5_padrao_definitivo.pdf", (7, 8, 9), kind="peça técnica — parecer", lines=60, points="20,00",
          required=("composição e instituição da equipe de planejamento", "normas e fases da contratação", "dispensa e condução da contratação", "pesquisa de preços"), theme="Contratação de equipamentos de TI no SISP", subthemes=("equipe de planejamento", "dispensa", "pesquisa de preços", "ETP", "fases da contratação"),
          situation="Divergências entre áreas administrativa e de TI na compra de servidores.", citations=("Lei n.º 14.133/2021", "IN SGD/ME n.º 94/2022", "SISP"), scope="específico", match="direta", item_indices=(96, 104, 105, 106, 107, 108), area=("GESTÃO E GOVERNANÇA DE TI", "CONTRATAÇÕES DE TI"),
          form=("situação-problema", "aplicação normativa", "peça técnica"), abstraction="misto", normative="sim", practical="sim", solution="sim", legislation="sim", norm_years=(2021, 2022)),

    qspec("tce_ac_2024_analista_ti_q1", "tce_ac_2024_analista_ti", "tce_ac_2024_cargos1a13_discursiva.pdf", (1,), "Internet: Getty Images.",
          "tce_ac_2024_cargos1a13_padrao_definitivo.pdf", (1,), kind="questão dissertativa", lines=30, points="20,00",
          required=("gestão pública e eficiência", "IA no controle institucional", "IA no controle social"), theme="Inteligência artificial no controle institucional e social", subthemes=("gestão pública", "eficiência", "controle institucional", "controle social"),
          situation="Discussão de aplicações de IA à fiscalização de recursos públicos.", citations=("inteligência artificial",), scope="geral", match="direta", item_indices=(64,), area=("INTELIGÊNCIA ARTIFICIAL",), form=("conceitual", "análise técnica"), practical="sim"),

    qspec("tcdf_2023_ace_sistemas_q1", "tcdf_2023_ace_sistemas", "tcdf_2023_cargo3_discursiva.pdf", (1,), "QUESTÃO 1",
          "tcdf_2023_cargo3_padrao_definitivo.pdf", (1, 2), kind="questão dissertativa", lines=20, points="10,00",
          required=("COBIT 2019 DSS05 e riscos", "ITIL v4 gerenciamento de incidentes", "OWASP: referência insegura a objeto e eavesdropping"), theme="Governança, serviços e segurança de TI", subthemes=("COBIT 2019 DSS05", "ITIL v4", "incidentes", "OWASP", "IDOR", "eavesdropping"),
          situation="Exposição integrada de referências de governança e segurança.", citations=("COBIT 2019", "ITIL v4", "OWASP"), scope="específico", match="parcial", item_indices=(91, 93, 100), area=("GESTÃO E GOVERNANÇA DE TI",), form=("conceitual",), normative="sim",
          notes="Correspondência parcial: COBIT 2019, ITIL v4 e cibersegurança constam do edital; os tópicos OWASP específicos não constam."),
    qspec("tcdf_2023_ace_sistemas_q2", "tcdf_2023_ace_sistemas", "tcdf_2023_cargo3_discursiva.pdf", (2,), "QUESTÃO 2",
          "tcdf_2023_cargo3_padrao_definitivo.pdf", (3, 4), kind="questão dissertativa", lines=20, points="10,00",
          required=("duas práticas XP", "visualização e WIP no Kanban", "duas reuniões Scrum"), theme="Metodologias ágeis de desenvolvimento", subthemes=("XP", "Kanban", "Scrum", "WIP", "eventos Scrum"),
          situation="Substituição de waterfall por abordagens ágeis em órgão público.", citations=("XP", "Kanban", "Scrum"), scope="específico", match="direta", item_indices=(26, 34, 36, 94), area=("ENGENHARIA DE SOFTWARE", "GESTÃO E GOVERNANÇA DE TI"), form=("situação-problema", "conceitual"), practical="sim", comparison="sim"),
    qspec("tcdf_2023_ace_sistemas_peca", "tcdf_2023_ace_sistemas", "tcdf_2023_cargo3_discursiva.pdf", (3,), "PEÇA DE NATUREZA TÉCNICA",
          "tcdf_2023_cargo3_padrao_definitivo.pdf", (5, 6), kind="peça de natureza técnica — parecer", lines=50, points="40,00",
          required=("introdução e características da LGPD", "controlador e responsabilidades", "operador e responsabilidades", "encarregado e responsabilidades", "quatro recomendações"), theme="Adequação institucional à LGPD", subthemes=("controlador", "operador", "encarregado", "tratamento de dados", "recomendações"),
          situation="Parecer para subsidiar atualização normativa do TCDF quanto à LGPD.", citations=("Lei n.º 13.709/2018", "Manual de Redação Oficial do TCDF"), scope="específico", match="direta", item_indices=(102,), area=("GESTÃO E GOVERNANÇA DE TI",), form=("aplicação normativa", "peça técnica"), abstraction="misto", normative="sim", practical="sim", solution="sim", legislation="sim", norm_years=(2018,)),

    qspec("tce_sc_2022_auditor_cc_relatorio", "tce_sc_2022_auditor_cc", "tce_sc_2021_cargo3_discursiva.pdf", (1, 2), "Estudantes",
          "tce_sc_2021_cargo3_padrao_definitivo.pdf", (1, 2, 3, 4), kind="peça técnica — relatório técnico", lines=90, points="40,00",
          required=("políticas e organização de segurança da informação", "segurança em recursos humanos", "controle de acesso"), theme="Sistema de gestão da segurança da informação", subthemes=("gestão de vulnerabilidades", "políticas", "recursos humanos", "controle de acesso", "riscos"),
          situation="Relatório técnico sobre programa de vulnerabilidades de universidade com muitos usuários e endpoints.", citations=("NBR ISO/IEC 27001:2013", "NBR ISO/IEC 27002"), scope="específico", match="direta", item_indices=(100,), area=("GESTÃO E GOVERNANÇA DE TI",),
          form=("estudo de caso", "aplicação normativa", "peça técnica"), abstraction="misto", normative="sim", practical="sim", solution="sim", legislation="não", norm_years=(2013,), end=None, decode_tcesc=True,
          notes="Texto recuperado do mapa de glifos do próprio PDF oficial; a normalização reverte a codificação deslocada sem resumir o conteúdo. O caderno imprime literalmente 'NBR2700'; a grafia foi preservada e não corrigida silenciosamente."),
    qspec("tce_ro_2019_ace_ti_q1", "tce_ro_2019_ace_ti", "tce_ro_2019_cargo1_discursiva.pdf", (1,), "A rápida e diversificada",
          "tce_ro_2019_cargo1_padrao_definitivo.pdf", (1, 2), kind="questão dissertativa", lines=30, points="40,00",
          required=("requisitos de segurança de sistemas", "princípios para projetar sistemas seguros", "ambiente seguro de desenvolvimento"), theme="Desenvolvimento seguro de sistemas", subthemes=("requisitos de segurança", "security by design", "ambiente de desenvolvimento", "MVP"),
          situation="Crítica à postergação de segurança e privacidade após o lançamento de MVP.", citations=("NBR ISO/IEC 27002:2013",), scope="específico", match="parcial", item_indices=(24, 35, 100), area=("ENGENHARIA DE SOFTWARE", "GESTÃO E GOVERNANÇA DE TI"),
          form=("aplicação normativa", "análise técnica"), normative="sim", practical="sim", norm_years=(2013,), notes="Correspondência parcial: cibersegurança e conceitos de projeto de software constam, mas desenvolvimento seguro não aparece como item autônomo."),

    qspec("tce_mg_2018_ace_cc_q1", "tce_mg_2018_ace_cc", "tce_mg_2018_cargo4_discursiva.pdf", (1,), "QUESTÃO 1",
          "tce_mg_2018_questao1_padrao_definitivo.pdf", (1, 2), kind="questão dissertativa", lines=60, points="20,00",
          required=("competências constitucionais privativas do TCU", "finalidades e objetivos da fiscalização financeira e orçamentária"), theme="Controle externo exercido pelos tribunais de contas", subthemes=("competências do TCU", "fiscalização financeira", "fiscalização orçamentária"),
          situation="Exposição constitucional sobre controle externo.", citations=("Constituição Federal",), scope="geral", match="inexistente", item_indices=(), area=(), form=("aplicação normativa", "conceitual"), normative="sim", legislation="sim", norm_years=(1988,)),
    qspec("tce_mg_2018_ace_cc_q2", "tce_mg_2018_ace_cc", "tce_mg_2018_cargo4_discursiva.pdf", (4,), "QUESTÃO 2",
          "tce_mg_2018_cargo4_questao2_padrao_definitivo.pdf", (1, 2, 3), kind="questão dissertativa", lines=60, points="20,00",
          required=("princípios do manifesto ágil", "qualidades de product owner", "qualidades de Scrum master", "planning poker", "modelo GROW"), theme="Scrum e práticas de equipes ágeis", subthemes=("manifesto ágil", "product owner", "Scrum master", "planning poker", "GROW"),
          situation="Exposição de princípios, papéis, estimativa e melhoria de desempenho.", citations=("Scrum", "planning poker", "GROW"), scope="específico", match="direta", item_indices=(26, 34, 36, 94), area=("ENGENHARIA DE SOFTWARE", "GESTÃO E GOVERNANÇA DE TI"), form=("conceitual",), normative="sim"),

    qspec("cgm_joao_pessoa_2018_auditor_sistemas_q1", "cgm_joao_pessoa_2018_auditor_sistemas", "cgm_joao_pessoa_2018_cargo3_discursiva.pdf", (1,), "A Infraestrutura de Chaves Públicas Brasileira",
          "cgm_joao_pessoa_2018_cargo3_padrao_definitivo.pdf", (1,), kind="questão dissertativa", lines=20, points="40,00",
          required=("consequências de quatro falhas do certificado", "solução para sanar os problemas"), theme="Certificados digitais e ICP-Brasil", subthemes=("autoridade certificadora", "expiração", "MD5", "nome DNS", "cadeia de confiança"),
          situation="Auditoria identifica certificado não confiável, expirado, com MD5 e nome incompatível.", citations=("ICP-Brasil", "MD5", "Firefox", "DNS"), scope="específico", match="apenas relacionada", item_indices=(100,), area=("GESTÃO E GOVERNANÇA DE TI",), form=("situação-problema", "análise técnica"), practical="sim", solution="sim", legislation="sim",
          notes="Certificação digital não é item expresso; há apenas relação conceitual com cibersegurança."),

    qspec("tce_pr_2016_analista_informatica_q1", "tce_pr_2016_analista_informatica", "tce_pr_2016_cargo8_discursiva.pdf", (1,), "QUESTÃO 1",
          "tce_pr_2016_cargo8_q1_padrao_preliminar.pdf", (1, 2), kind="questão dissertativa", lines=15, points="5,00",
          required=("atividades de análise econômica, requisitos e especificação", "três artefatos", "três diagramas"), theme="Fases e artefatos de engenharia de software", subthemes=("análise econômica", "requisitos", "especificação", "artefatos", "diagramas UML"),
          situation="Gerente planeja software de controle de vendas de automóveis.", citations=("engenharia de software", "UML"), scope="específico", match="direta", item_indices=(24, 27), area=("ENGENHARIA DE SOFTWARE",), form=("situação-problema", "conceitual"), practical="sim", diagram="não", notes="A questão exige citar nomes de diagramas, não desenhá-los. Padrão oficial disponível apenas em versão preliminar."),
    qspec("tce_pr_2016_analista_informatica_q2", "tce_pr_2016_analista_informatica", "tce_pr_2016_cargo8_discursiva.pdf", (2,), "QUESTÃO 2",
          "tce_pr_2016_cargo8_q2_padrao_preliminar.pdf", (1,), kind="questão dissertativa", lines=15, points="5,00",
          required=("objetivo da metodologia de processos", "atividades da metodologia", "função de duas atividades"), theme="Processos de engenharia de software", subthemes=("comunicação", "planejamento", "modelagem", "construção", "emprego"),
          situation="Exposição sobre camada de processos da engenharia de software.", citations=("engenharia de software",), scope="específico", match="parcial", item_indices=(24,), area=("ENGENHARIA DE SOFTWARE",), form=("conceitual",), notes="Padrão oficial disponível apenas em versão preliminar; o edital atual cobre projeto de software, não explicita a estrutura específica de processo cobrada."),
    qspec("tce_pr_2016_analista_informatica_q3", "tce_pr_2016_analista_informatica", "tce_pr_2016_cargo8_discursiva.pdf", (3,), "QUESTÃO 3",
          "tce_pr_2016_cargo8_q3_padrao_preliminar.pdf", (1,), kind="questão dissertativa", lines=15, points="5,00",
          required=("comportamento do remetente em partida lenta", "detecção e reação ao congestionamento", "finalização da partida lenta"), theme="Controle de congestionamento TCP", subthemes=("slow start", "janela de congestionamento", "timeout", "ACK"),
          situation="Exposição técnica de protocolo de transporte.", citations=("TCP",), scope="específico", match="inexistente", item_indices=(), area=(), form=("conceitual",), notes="Padrão oficial disponível apenas em versão preliminar."),
    qspec("tce_pr_2016_analista_informatica_q4", "tce_pr_2016_analista_informatica", "tce_pr_2016_cargo8_discursiva.pdf", (4,), "QUESTÃO 4",
          "tce_pr_2016_cargo8_q4_padrao_preliminar.pdf", (1,), kind="questão dissertativa", lines=15, points="5,00",
          required=("importância dos níveis de capacidade COBIT 5 e relação com ISO/IEC 15504", "número, nome e características dos níveis"), theme="Níveis de capacidade do COBIT 5", subthemes=("capacidade de processos", "ISO/IEC 15504"),
          situation="Exposição normativa sobre avaliação de capacidade.", citations=("COBIT 5", "ISO/IEC 15504"), scope="específico", match="parcial", item_indices=(91,), area=("GESTÃO E GOVERNANÇA DE TI",), form=("aplicação normativa", "conceitual"), normative="sim", norm_years=(2012,), notes="O edital atual explicita COBIT 2019, não COBIT 5; padrão oficial apenas preliminar."),
    qspec("tce_pr_2016_analista_informatica_peca", "tce_pr_2016_analista_informatica", "tce_pr_2016_cargo8_discursiva.pdf", (5,), "PARECER",
          "tce_pr_2016_cargo8_parecer_padrao_preliminar.pdf", (1,), kind="peça técnica — parecer", lines=60, points="20,00",
          required=("qualidade de software", "método ágil", "gerenciamento de projetos e estimativas"), theme="Avaliação de relatório sobre qualidade, agilidade, projetos e métricas", subthemes=("CMMI-DEV", "MPS.BR", "Scrum", "XP", "Kanban", "PMBOK", "APF"),
          situation="Parecer sobre proposições corretas e incorretas de consultoria de software.", citations=("CMMI-DEV 1.2", "MPS.BR 2016", "Scrum 2016", "PMBOK 5", "APF 4.3"), scope="específico", match="parcial", item_indices=(26, 36, 41, 94), area=("ENGENHARIA DE SOFTWARE", "GESTÃO E GOVERNANÇA DE TI"),
          form=("estudo de caso", "análise técnica", "peça técnica"), abstraction="misto", normative="sim", practical="sim", comparison="sim", calculation="não", norm_years=(2016,), notes="A análise de ponto de função é avaliada conceitualmente; não há cálculo. CMMI e MPS.BR não constam do edital atual; Scrum, métricas e gestão de projetos constam. Padrão oficial apenas preliminar."),

    qspec("tce_pa_2016_auditor_informatica_q1", "tce_pa_2016_auditor_informatica", "tce_pa_2016_cargos1e18a38_discursiva.pdf", (1,), "O resultado mais significativo",
          "tce_pa_2016_cargos1e18a38_padrao_definitivo.pdf", (1,), kind="questão dissertativa", lines=30, points="10,00",
          required=("conceito de desenvolvimento sustentável", "decisões presentes e futuro", "sustentabilidade na gestão municipal"), theme="Desenvolvimento sustentável e gestão municipal", subthemes=("Agenda 2030", "sustentabilidade", "gestão municipal"),
          situation="Tema geral comum a cinco especialidades superiores de TI.", citations=("Agenda 2030",), scope="geral", match="inexistente", item_indices=(), area=(), form=("conceitual",), exact_specialty="Informática — Administrador de Banco de Dados; Analista de Segurança; Analista de Sistema; Analista de Suporte; Web Design — cargos 32 a 36"),

    qspec("tcu_2015_aufc_ti_p3_q1", "tcu_2015_aufc_ti", "tcu_2015_p3_comum_discursiva.pdf", (1,), "QUESTÃO 1",
          "tcu_2015_p3_q1_padrao_definitivo.pdf", (1,), kind="questão dissertativa", lines=20, points="20,00",
          required=("equilíbrio entre confidencialidade e transparência", "responsabilidades do auditor", "requisições de terceiros"), theme="Confidencialidade e transparência na documentação de auditoria", subthemes=("documentação", "responsabilidade do auditor", "acesso por terceiros"),
          situation="Exposição de normas de auditoria do setor público.", citations=("INTOSAI", "ISSAI 1230"), scope="geral", match="apenas relacionada", item_indices=(101,), area=("GESTÃO E GOVERNANÇA DE TI",), form=("aplicação normativa", "conceitual"), normative="sim", notes="Relação apenas conceitual com a Lei de Acesso à Informação; a questão aplica norma INTOSAI."),
    qspec("tcu_2015_aufc_ti_p3_q2", "tcu_2015_aufc_ti", "tcu_2015_p3_comum_discursiva.pdf", (3,), "QUESTÃO 2",
          "tcu_2015_p3_q2_padrao_definitivo.pdf", (1,), kind="questão dissertativa", lines=20, points="20,00",
          required=("independência como requisito essencial", "limites da independência", "independência dos integrantes"), theme="Independência das entidades fiscalizadoras superiores", subthemes=("Declaração de Lima", "controle", "independência funcional"),
          situation="Exposição sobre auditoria governamental independente.", citations=("INTOSAI", "Declaração de Lima"), scope="geral", match="inexistente", item_indices=(), area=(), form=("aplicação normativa", "conceitual"), normative="sim"),
    qspec("tcu_2015_aufc_ti_p4_q1", "tcu_2015_aufc_ti", "tcu_2015_cargo2_p4_discursiva.pdf", (1,), "QUESTÃO – CONHECIMENTOS ESPECÍFICOS",
          "tcu_2015_cargo2_p4_questao_padrao_definitivo.pdf", (1,), kind="questão dissertativa", lines=20, points="20,00",
          required=("atividades de identificação de riscos", "itens identificados em cada atividade para a organização"), theme="Identificação de riscos de segurança da informação", subthemes=("ativos", "ameaças", "vulnerabilidades", "consequências", "controles existentes"),
          situation="Empresa digital com centro de dados único, ameaças e alta dependência de continuidade.", citations=("NBR ISO/IEC 27005:2011",), scope="específico", match="parcial", item_indices=(92, 100), area=("GESTÃO E GOVERNANÇA DE TI",), form=("estudo de caso", "aplicação normativa", "análise técnica"), normative="sim", practical="sim", norm_years=(2011,), notes="O edital cobre gestão de riscos e cibersegurança, mas explicita ISO 31000/COSO e ISO 27001/27002/NIST, não ISO 27005."),
    qspec("tcu_2015_aufc_ti_p4_peca", "tcu_2015_aufc_ti", "tcu_2015_cargo2_p4_discursiva.pdf", (3,), "PEÇA DE NATUREZA TÉCNICA",
          "tcu_2015_cargo2_p4_peca_padrao_definitivo.pdf", (1, 2), kind="peça de natureza técnica — parecer", lines=50, points="40,00",
          required=("conformidade do PDTI", "conformidade de sete contratos de soluções de TI"), theme="Contratação e gestão de contratos de soluções de TI", subthemes=("PDTI", "cooperativa", "atos administrativos", "segurança", "métricas", "prorrogação", "nível de serviço"),
          situation="Parecer de auditoria sobre sete contratos de TI de órgão do SISP.", citations=("IN SLTI/MPOG n.º 2/2008", "IN SLTI/MP n.º 4/2014", "SISP"), scope="específico", match="parcial", item_indices=(95, 96, 104, 105), area=("GESTÃO E GOVERNANÇA DE TI", "CONTRATAÇÕES DE TI"),
          form=("estudo de caso", "aplicação normativa", "peça técnica"), abstraction="misto", normative="sim", practical="sim", solution="sim", legislation="sim", norm_years=(2008, 2014,), notes="Correspondência parcial: contratação e planejamento de TI permanecem no edital, mas as instruções normativas cobradas foram substituídas pelas normas atuais nele explicitadas."),

    qspec("tcu_2026_aufc_auditoria_ti_q1", "tcu_2026_aufc_auditoria_ti", "tcu_2025_discursiva.pdf", (1,), "Questão 1",
          "tcu_2025_padrao_definitivo.pdf", (1, 2), kind="questão dissertativa", lines=20, points="10,00",
          required=("responsabilidade civil do Estado e direito de regresso", "competência do TCU em prejuízo ao erário"), theme="Responsabilidade civil do Estado e competências do TCU", subthemes=("risco administrativo", "direito de regresso", "débito", "multa"),
          situation="Exposição jurídica geral da prova do cargo de Auditoria de TI.", citations=("Constituição Federal",), scope="geral", match="inexistente", item_indices=(), area=(), form=("aplicação normativa", "conceitual"), normative="sim", legislation="sim", norm_years=(1988,)),
    qspec("tcu_2026_aufc_auditoria_ti_q2", "tcu_2026_aufc_auditoria_ti", "tcu_2025_discursiva.pdf", (2,), "Questão 2",
          "tcu_2025_padrao_definitivo.pdf", (3, 4), kind="questão dissertativa", lines=20, points="10,00",
          required=("duas falhas que comprometem a confidencialidade", "duas medidas corretivas para o pipeline MLOps"), theme="Segurança de pipeline MLOps em nuvem", subthemes=("contêineres", "buckets", "privilégio mínimo", "logs", "IA generativa", "deploy"),
          situation="Contêiner de inferência acessa documentos fora do escopo após atualização sem revisão de segurança.", citations=("MLOps", "IA generativa", "contêineres", "nuvem"), scope="específico", match="direta", item_indices=(45, 66, 69, 100), area=("ENGENHARIA DE SOFTWARE", "INTELIGÊNCIA ARTIFICIAL", "GESTÃO E GOVERNANÇA DE TI"),
          form=("situação-problema", "análise técnica"), practical="sim", solution="sim", conceptual="não"),
    qspec("tcu_2026_aufc_auditoria_ti_q3", "tcu_2026_aufc_auditoria_ti", "tcu_2025_discursiva.pdf", (3,), "Questão 3",
          "tcu_2025_padrao_definitivo.pdf", (5,), kind="questão dissertativa", lines=20, points="10,00",
          required=("conformidade dos papéis de product owner e Scrum master", "pertinência de TDD e aplicação de DDD"), theme="Scrum, TDD e DDD em auditoria de software", subthemes=("product owner", "Scrum master", "backlog", "TDD", "DDD", "regras de negócio"),
          situation="Papéis Scrum invertidos e testes realizados somente após a codificação.", citations=("Guia Scrum", "TDD", "DDD"), scope="específico", match="parcial", item_indices=(26, 36, 37, 38, 94), area=("ENGENHARIA DE SOFTWARE", "GESTÃO E GOVERNANÇA DE TI"),
          form=("situação-problema", "análise técnica"), normative="sim", practical="sim", comparison="sim", notes="Scrum e testes constam diretamente; TDD e DDD não são explicitados no edital."),
    qspec("tcu_2026_aufc_auditoria_ti_peca", "tcu_2026_aufc_auditoria_ti", "tcu_2025_discursiva.pdf", (4,), "Peça de Natureza Técnica",
          "tcu_2025_padrao_definitivo.pdf", (6, 7), kind="peça de natureza técnica — parecer", lines=50, points="30,00",
          required=("TCO e formação do preço estimado", "pagamento, SLA, reversibilidade e proteção de dados", "segregação e qualificação dos fiscais", "conclusão e medidas corretivas"), theme="Auditoria de contratação de solução SaaS", subthemes=("ETP", "TCO", "pesquisa de preços", "SLA", "glosas", "lock-in", "dados pessoais", "segregação de funções"),
          situation="Três achados em contratação de SaaS para gestão documental.", citations=("Lei n.º 14.133/2021", "IN SGD/ME n.º 94/2022", "LGPD", "SaaS"), scope="específico", match="direta", item_indices=(96, 102, 104, 105, 106, 107, 108), area=("GESTÃO E GOVERNANÇA DE TI", "CONTRATAÇÕES DE TI"),
          form=("estudo de caso", "aplicação normativa", "peça técnica"), abstraction="misto", normative="sim", practical="sim", solution="sim", comparison="sim", legislation="sim", norm_years=(2018, 2021, 2022)),

    qspec("sefaz_se_2025_auditor_ti_q1", "sefaz_se_2025_auditor_ti", "sefaz_se_2025_especialidade2_q1_discursiva.pdf", (1,), "Questão 1",
          "sefaz_se_2025_especialidade2_q1_padrao_definitivo.pdf", (1, 2), kind="questão dissertativa", lines=20, points="40,00",
          required=("quatro etapas do desenvolvimento de modelo preditivo", "overfitting e underfitting", "métricas e validação"), theme="Modelagem preditiva", subthemes=("pré-processamento", "seleção de variáveis", "treinamento", "validação", "overfitting", "underfitting"),
          situation="Exposição do ciclo de construção e validação de modelos.", citations=("aprendizado de máquina", "modelagem preditiva"), scope="específico", match="direta", item_indices=(51, 52, 53, 57, 65), area=("ANÁLISE DE DADOS", "INTELIGÊNCIA ARTIFICIAL"), form=("conceitual", "análise técnica"), comparison="sim", calculation="não"),
    qspec("sefaz_se_2025_auditor_ti_q2", "sefaz_se_2025_auditor_ti", "sefaz_se_2025_especialidade2_q2_discursiva.pdf", (1,), "Questão 2",
          "sefaz_se_2025_especialidade2_q2_padrao_definitivo.pdf", (1, 2), kind="questão dissertativa", lines=20, points="40,00",
          required=("definição, elementos e esquemas OLAP", "funcionamento, etapas e técnicas de ETL"), theme="OLAP e ETL", subthemes=("cubos", "dimensões", "medidas", "ROLAP", "MOLAP", "extração", "transformação", "carga"),
          situation="Exposição de arquitetura analítica e ingestão de dados.", citations=("OLAP", "ETL"), scope="específico", match="parcial", item_indices=(15, 23, 48), area=("ENGENHARIA DE DADOS", "ANÁLISE DE DADOS"), form=("conceitual",), notes="ETL e modelagem dimensional constam diretamente; OLAP e seus esquemas de armazenamento não são explicitados."),

    qspec("sefa_pr_2026_agente_ti_q1", "sefa_pr_2026_agente_ti", "sefa_pr_2025_discursiva.pdf", (1,), "A administração pública contemporânea",
          "sefa_pr_2025_padrao_definitivo.pdf", (1, 2), kind="questão dissertativa", lines=30, points="15,00",
          required=("SWOT em estratégias GovTech", "governança digital, accountability e transparência", "design thinking e valor público"), theme="Planejamento e transformação digital no setor público", subthemes=("SWOT", "GovTech", "governança digital", "accountability", "design thinking", "valor público"),
          situation="Integração de planejamento estratégico e inovação pública.", citations=("SWOT", "GovTech", "design thinking"), scope="geral", match="apenas relacionada", item_indices=(28, 32, 95, 99), area=("ENGENHARIA DE SOFTWARE", "GESTÃO E GOVERNANÇA DE TI"), form=("conceitual", "análise técnica"), practical="sim", notes="Os conceitos específicos SWOT, GovTech e design thinking não são itens expressos; há relação com planejamento e projeto centrado no usuário."),

    qspec("sefaz_ce_2021_auditor_ti_q1", "sefaz_ce_2021_auditor_ti", "sefaz_ce_2021_cargo4_discursiva.pdf", (1,), "QUESTÃO 1",
          "sefaz_ce_2021_cargo4_padrao_definitivo.pdf", (1,), kind="questão dissertativa", lines=20, points="2,50",
          required=("definição e funcionamento do Hadoop", "dois componentes do ecossistema"), theme="Apache Hadoop e processamento distribuído", subthemes=("HDFS", "MapReduce", "YARN", "cluster", "tolerância a falhas"),
          situation="Exposição técnica sobre ecossistema de big data.", citations=("Apache Hadoop",), scope="específico", match="parcial", item_indices=(9,), area=("ENGENHARIA DE DADOS",), form=("conceitual",), notes="O edital prevê ingestão e armazenamento de big data, mas não explicita Hadoop."),
    qspec("sefaz_ce_2021_auditor_ti_q2", "sefaz_ce_2021_auditor_ti", "sefaz_ce_2021_cargo4_discursiva.pdf", (2,), "QUESTÃO 2",
          "sefaz_ce_2021_cargo4_padrao_definitivo.pdf", (2, 3), kind="questão dissertativa", lines=20, points="2,50",
          required=("dois tipos de redes neurais", "duas etapas de PLN", "retropropagação e componentes de ativação"), theme="Deep learning e processamento de linguagem natural", subthemes=("redes neurais", "PLN", "retropropagação", "função de ativação"),
          situation="Exposição de arquiteturas e treinamento de redes neurais.", citations=("deep learning", "machine learning", "PLN"), scope="específico", match="direta", item_indices=(65, 67, 68), area=("INTELIGÊNCIA ARTIFICIAL",), form=("conceitual", "análise técnica"), comparison="sim"),
    qspec("sefaz_ce_2021_auditor_ti_estudo", "sefaz_ce_2021_auditor_ti", "sefaz_ce_2021_cargo4_discursiva.pdf", (3,), "ESTUDO DE CASO",
          "sefaz_ce_2021_cargo4_padrao_definitivo.pdf", (4, 5), kind="estudo de caso", lines=45, points="5,00",
          required=("avaliar achados e proposições sobre PMBOK", "avaliar Scrum", "avaliar XP", "avaliar COBIT 2019"), theme="Avaliação de maturidade ágil e governança de TI", subthemes=("PMBOK 6", "Scrum 2020", "XP", "COBIT 2019", "requisitos", "cronograma", "papéis"),
          situation="Auditor avalia relatório de consultoria com achados e proposições sobre métodos e governança.", citations=("PMBOK 6", "Scrum 2020", "XP", "COBIT 2019"), scope="específico", match="parcial", item_indices=(26, 34, 36, 91, 94), area=("ENGENHARIA DE SOFTWARE", "GESTÃO E GOVERNANÇA DE TI"),
          form=("estudo de caso", "análise técnica", "aplicação normativa"), abstraction="misto", normative="sim", practical="sim", comparison="sim", norm_years=(2019, 2020,), notes="Há correspondência direta com COBIT e Scrum/gestão de projetos, mas versões e XP divergem do detalhamento atual."),

    qspec("stj_2024_analista_ti_cargo3", "stj_2024_analista_ti", "stj_2024_cargo3_discursiva.pdf", (1,), "Uma empresa de tecnologia",
          "stj_2024_cargo3_padrao_definitivo.pdf", (1, 2), kind="questão dissertativa", lines=30, points="40,00",
          required=("impactos de falhas nos controles internos", "impactos de deficiências de governança", "princípios e objetivos do COBIT 2019", "medidas de implementação"), theme="Implementação do COBIT 2019", subthemes=("controles internos", "governança", "riscos", "objetivos de governança e gestão"),
          situation="Empresa decide implantar COBIT após auditoria revelar falhas e riscos.", citations=("COBIT 2019",), scope="específico", match="direta", item_indices=(91,), area=("GESTÃO E GOVERNANÇA DE TI",), form=("situação-problema", "análise técnica", "aplicação normativa"), normative="sim", practical="sim", solution="sim", exact_specialty="Análise de Sistemas de Informação — cargo 3"),
    qspec("stj_2024_analista_ti_cargo18", "stj_2024_analista_ti", "stj_2024_cargo18_discursiva.pdf", (1,), "A criptografia é",
          "stj_2024_cargo18_padrao_definitivo.pdf", (1,), kind="questão dissertativa", lines=30, points="40,00",
          required=("criptografia simétrica e assimétrica", "certificado digital e dois usos", "hash e seus princípios"), theme="Criptografia, certificados digitais e hash", subthemes=("chave simétrica", "chave assimétrica", "PKI", "certificados", "integridade", "hash"),
          situation="Exposição conceitual de mecanismos criptográficos.", citations=("criptografia", "certificado digital", "hash"), scope="específico", match="parcial", item_indices=(100,), area=("GESTÃO E GOVERNANÇA DE TI",), form=("conceitual",), comparison="sim", exact_specialty="Suporte em Tecnologia da Informação — cargo 18", notes="Cibersegurança é expressa, mas os mecanismos criptográficos não são detalhados no edital."),

    qspec("trt10_2025_analista_ti_q1", "trt10_2025_analista_ti", "trt10_2024_cargo11_discursiva.pdf", (1,), "O desenvolvimento de software seguro",
          "trt10_2024_cargo11_padrao_definitivo.pdf", (1, 2), kind="questão dissertativa", lines=30, points="30,00",
          required=("pressupostos fundamentais do DevSecOps", "objetivos do OWASP SAMM", "benefícios de CI/CD", "práticas de segurança no ciclo"), theme="DevSecOps e OWASP SAMM", subthemes=("cultura", "segurança por design", "CI/CD", "maturidade", "testes de segurança"),
          situation="Discussão de segurança contínua no ciclo de desenvolvimento.", citations=("DevSecOps", "OWASP SAMM", "CI/CD"), scope="específico", match="parcial", item_indices=(37, 38, 42, 43, 44, 100), area=("ENGENHARIA DE SOFTWARE", "GESTÃO E GOVERNANÇA DE TI"),
          form=("conceitual", "análise técnica"), normative="sim", practical="sim", notes="DevOps, CI/CD, testes e cibersegurança constam; DevSecOps e OWASP SAMM não aparecem nominalmente."),

    qspec("trf6_2025_analistas_ti_q1", "trf6_2025_analistas_ti", "trf6_2024_cargos_superiores_comum_discursiva.pdf", (1,), "A doença do planeta Terra",
          "trf6_2024_cargos_superiores_comum_padrao_definitivo.pdf", (1, 2), kind="questão dissertativa", lines=30, points="20,00",
          required=("atores no enfrentamento da emergência climática", "impactos atuais e ações presentes", "ações de médio e longo prazo"), theme="Emergência climática e sustentabilidade", subthemes=("mudanças climáticas", "cooperação", "políticas públicas", "sustentabilidade"),
          situation="Tema geral comum aos cargos superiores, inclusive quatro especialidades de TI.", citations=("mudanças climáticas",), scope="geral", match="inexistente", item_indices=(), area=(), form=("conceitual",), exact_specialty="Análise de Dados; Análise de Sistemas de Informação; Governança e Gestão de TI; Tecnologia da Informação — cargos 2, 3, 13 e 22"),
]


def event_for_file(filename: str) -> str:
    matches = []
    for event in MANIFEST:
        if any(Path(d["arquivo_local"]).name == filename for d in event["documentos"]):
            matches.append(event["identificador_api"])
    if len(matches) != 1:
        raise RuntimeError(f"Arquivo sem evento unico no manifesto: {filename}")
    return matches[0]


def extract_quesitos(pattern_text: str) -> str:
    marker = re.search(r"QUESITOS AVALIADOS", pattern_text, flags=re.I)
    return pattern_text[marker.start():].strip() if marker else pattern_text.strip()


def score_distribution(statement: str, pattern: str, total: str) -> str:
    values = re.findall(r"\[\s*valor\s*:\s*[^\]]+\]", statement, flags=re.I)
    if not values:
        values = re.findall(r"\b(?:valor|pontuação)[^\n.;]{0,80}\b\d+[,.]\d+\s*pontos?", pattern, flags=re.I)
    return json.dumps({"pontuacao_total": total, "valores_explicitos_no_enunciado": values}, ensure_ascii=False)


def build_phase2_questions(contests: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for spec in Q_SPECS:
        event = event_for_file(spec["proof"])
        proof_doc = doc(event, spec["proof"])
        pattern_doc = doc(event, spec["pattern"])
        statement_source = pdf_text(proof_doc["arquivo_local"], spec["proof_pages"], spec["decode_tcesc"])
        statement = excerpt(statement_source, spec["start"], spec["end"])
        pattern_text = pdf_text(pattern_doc["arquivo_local"], spec["pattern_pages"])
        contest = contests[spec["cid"]]
        pattern_version = "preliminar" if "preliminar" in spec["pattern"] else "definitivo"
        notes = spec["notes"]
        if pattern_version == "preliminar" and "preliminar" not in notes.casefold():
            notes = (notes + " Padrão de resposta oficial disponível somente em versão preliminar.").strip()
        rows.append({
            "id_questao": spec["qid"], "id_concurso": spec["cid"], "ano": contest["ano"],
            "orgao": contest["orgao"], "cargo": spec["exact_cargo"] or contest["cargo"],
            "especialidade": spec["exact_specialty"] or contest["especialidade"],
            "tipo_discursiva": spec["kind"], "numero_maximo_linhas": spec["lines"],
            "pontuacao": spec["points"], "enunciado_integral": statement,
            "itens_exigidos": jlist(*spec["required"]), "tema_principal": spec["theme"],
            "subtemas": jlist(*spec["subthemes"]), "situacao_problema": spec["situation"],
            "norma_ou_tecnologia_citada": jlist(*spec["citations"]),
            "conhecimento_geral_ou_especifico": spec["scope"],
            "correspondencia_com_edital_tce_ma": spec["match"],
            "itens_correspondentes_tce_ma": mapped(*spec["item_indices"]),
            "texto_padrao_resposta": pattern_text,
            "url_prova": proof_doc["url"], "url_padrao_resposta": pattern_doc["url"],
            "fonte_enunciado": f"caderno oficial, PDF p. {', '.join(map(str, spec['proof_pages']))}",
            "fonte_padrao_resposta": f"padrão {pattern_version} oficial, PDF p. {', '.join(map(str, spec['pattern_pages']))}",
            "status_confirmacao": "confirmado", "observacoes": notes,
            "area_tce_ma": jlist(*spec["area"]), "forma_cobranca": jlist(*spec["form"]),
            "nivel_abstracao": spec["abstraction"],
            "exige_memorizacao_normativa": spec["normative"],
            "exige_aplicacao_pratica": spec["practical"],
            "exige_proposta_solucao": spec["solution"], "exige_comparacao": spec["comparison"],
            "exige_explicacao_conceitual": spec["conceptual"], "exige_calculo": spec["calculation"],
            "exige_codigo": spec["code"], "exige_diagrama": spec["diagram"],
            "exige_conhecimento_legislacao": spec["legislation"],
            "ano_norma_cobrada": jlist(*spec["norm_years"]),
            "quesitos_avaliados": extract_quesitos(pattern_text),
            "distribuicao_pontos_padrao": score_distribution(statement, pattern_text, spec["points"]),
        })
    return rows


BASE_PATTERN_PAGES = {
    "tce_rj_2021_ace_ti_q1": ("fontes/padroes_resposta/tce_rj_2021_cargo4_padrao_definitivo.pdf", (1, 2)),
    "tce_rj_2021_ace_ti_q2": ("fontes/padroes_resposta/tce_rj_2021_cargo4_padrao_definitivo.pdf", (3, 4)),
    "tce_rj_2021_ace_ti_q3": ("fontes/padroes_resposta/tce_rj_2021_cargo4_padrao_definitivo.pdf", (5,)),
    "tce_rj_2021_ace_ti_peca": ("fontes/padroes_resposta/tce_rj_2021_cargo4_padrao_definitivo.pdf", (6, 7, 8)),
    "tcdf_2024_ace_ti_infra_q1": ("fontes/padroes_resposta/tcdf_2024_especialidade3_padrao_definitivo.pdf", (1,)),
    "tcdf_2024_ace_ti_infra_q2": ("fontes/padroes_resposta/tcdf_2024_especialidade3_padrao_definitivo.pdf", (2, 3)),
    "tcdf_2024_ace_ti_infra_peca": ("fontes/padroes_resposta/tcdf_2024_especialidade3_padrao_definitivo.pdf", (4, 5)),
    "tce_ms_2025_ace_ti_q1": ("fontes/padroes_resposta/tce_ms_2025_cargo5_padrao_definitivo.pdf", (1, 2)),
    "tce_ms_2025_ace_ti_q2": ("fontes/padroes_resposta/tce_ms_2025_cargo5_padrao_definitivo.pdf", (3, 4)),
    "tce_ms_2025_ace_ti_q3": ("fontes/padroes_resposta/tce_ms_2025_cargo5_padrao_definitivo.pdf", (5,)),
    "tce_ms_2025_ace_ti_peca": ("fontes/padroes_resposta/tce_ms_2025_cargo5_padrao_definitivo.pdf", (6, 7)),
}


BASE_FORMS = {
    "tce_rj_2021_ace_ti_q1": ("situação-problema", "aplicação normativa"),
    "tce_rj_2021_ace_ti_q2": ("situação-problema", "conceitual"),
    "tce_rj_2021_ace_ti_q3": ("situação-problema", "análise técnica"),
    "tce_rj_2021_ace_ti_peca": ("estudo de caso", "aplicação normativa", "peça técnica"),
    "tcdf_2024_ace_ti_infra_q1": ("situação-problema", "análise técnica"),
    "tcdf_2024_ace_ti_infra_q2": ("aplicação normativa", "conceitual"),
    "tcdf_2024_ace_ti_infra_peca": ("situação-problema", "análise técnica", "peça técnica"),
    "tce_ms_2025_ace_ti_q1": ("análise técnica", "projeto/arquitetura"),
    "tce_ms_2025_ace_ti_q2": ("aplicação normativa", "conceitual"),
    "tce_ms_2025_ace_ti_q3": ("situação-problema", "análise técnica"),
    "tce_ms_2025_ace_ti_peca": ("estudo de caso", "aplicação normativa", "peça técnica"),
}


def extend_phase1_questions(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    for row in rows:
        qid = row["id_questao"]
        mapped_items = json.loads(row["itens_correspondentes_tce_ma"])
        areas = list(dict.fromkeys(item.split(" — ", 1)[0] for item in mapped_items))
        citations = " ".join(json.loads(row["norma_ou_tecnologia_citada"]))
        years = sorted({int(y) for y in re.findall(r"(?:19|20)\d{2}", citations)})
        pattern_path, pattern_pages = BASE_PATTERN_PAGES[qid]
        exact_pattern = pdf_text(pattern_path, pattern_pages)
        forms = BASE_FORMS[qid]
        is_piece = "peça técnica" in forms
        normative = bool(re.search(r"\b(?:Lei|IN |Instrução|ITIL|COBIT|ISO|Manual)\b", citations, re.I))
        legislation = bool(re.search(r"\b(?:Lei|IN |Instrução|Constituição)\b", citations, re.I))
        row.update({
            "area_tce_ma": jlist(*areas), "forma_cobranca": jlist(*forms),
            "nivel_abstracao": "misto" if is_piece else "médio",
            "exige_memorizacao_normativa": "sim" if normative else "não",
            "exige_aplicacao_pratica": "sim" if "situação-problema" in forms or is_piece or "análise técnica" in forms else "não",
            "exige_proposta_solucao": "sim" if qid in {"tce_rj_2021_ace_ti_q3", "tce_rj_2021_ace_ti_peca", "tce_ms_2025_ace_ti_peca"} else "não",
            "exige_comparacao": "sim" if qid in {"tce_rj_2021_ace_ti_q1", "tcdf_2024_ace_ti_infra_q1", "tcdf_2024_ace_ti_infra_peca"} else "não",
            "exige_explicacao_conceitual": "sim", "exige_calculo": "não", "exige_codigo": "não",
            "exige_diagrama": "não", "exige_conhecimento_legislacao": "sim" if legislation else "não",
            "ano_norma_cobrada": jlist(*years), "quesitos_avaliados": extract_quesitos(exact_pattern),
            "distribuicao_pontos_padrao": score_distribution(str(row["enunciado_integral"]), exact_pattern, str(row["pontuacao"])),
        })
    return rows


RESEARCHED_NOT_INCLUDED = [
    {"evento": "CNJ_24", "status": "elegível, não incorporado", "motivo": "Substituído antes da classificação temática pelo TCU_25_AUFC, de prioridade 1 e maior comparabilidade; PDFs oficiais preservados em fontes/."},
    {"evento": "SEFIN_FORTALEZA_CE_23", "status": "elegível, não incorporado", "motivo": "Teto de 20 novos concursos atingido com certames de maior prioridade; discursiva era geral e comum aos analistas."},
    {"evento": "CGE_CE_18", "status": "rejeitado", "motivo": "Cargo de TI identificado, mas sem prova discursiva."},
    {"evento": "CGE_RJ_23", "status": "rejeitado", "motivo": "Cargo genérico de Auditor do Estado; especialidade de TI não confirmada documentalmente."},
    {"evento": "TCE_PE_17", "status": "rejeitado", "motivo": "Não foi localizado cargo superior de TI no certame."},
    {"evento": "TCE_PB_17", "status": "rejeitado", "motivo": "Documentação não confirmou especialidade de TI; referência apenas genérica a demais áreas."},
    {"evento": "SEFAZ_AL_19 / SEFAZ_AL_21 / SEFAZ_RR_21 / SEFAZ_SE_21 / SEFAZ_RN_25 / SEFAZ_RJ_25_AUDITOR", "status": "rejeitado", "motivo": "Cargos fiscais genéricos, sem especialidade de TI documentalmente confirmada."},
    {"evento": "SEFAZ_RJ_25_ANALISTA", "status": "rejeitado", "motivo": "Especialidades administrativas, contábeis, econômicas e financeiras; não havia cargo de TI."},
    {"evento": "SERPRO_23 / DATAPREV_23", "status": "rejeitado", "motivo": "Cargos de TI presentes, mas a API oficial não disponibilizou caderno discursivo; componente discursivo não confirmado."},
]


CONTEST_FIELDS = [
    "id_concurso", "ano", "orgao", "cargo", "especialidade", "banca", "tipo_orgao", "nivel_cargo",
    "categoria_comparabilidade", "url_edital", "url_prova", "url_padrao_resposta", "fonte_oficial",
    "status_confirmacao", "observacoes",
]
QUESTION_FIELDS = [
    "id_questao", "id_concurso", "ano", "orgao", "cargo", "especialidade", "tipo_discursiva",
    "numero_maximo_linhas", "pontuacao", "enunciado_integral", "itens_exigidos", "tema_principal",
    "subtemas", "situacao_problema", "norma_ou_tecnologia_citada", "conhecimento_geral_ou_especifico",
    "correspondencia_com_edital_tce_ma", "itens_correspondentes_tce_ma", "texto_padrao_resposta",
    "url_prova", "url_padrao_resposta", "fonte_enunciado", "fonte_padrao_resposta", "status_confirmacao",
    "observacoes", "area_tce_ma", "forma_cobranca", "nivel_abstracao",
    "exige_memorizacao_normativa", "exige_aplicacao_pratica", "exige_proposta_solucao",
    "exige_comparacao", "exige_explicacao_conceitual", "exige_calculo", "exige_codigo",
    "exige_diagrama", "exige_conhecimento_legislacao", "ano_norma_cobrada", "quesitos_avaliados",
    "distribuicao_pontos_padrao",
]


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    base_contests, base_questions = load_phase1()
    phase2_contests, contest_map = build_contests()
    phase2_questions = build_phase2_questions(contest_map)
    if len(phase2_contests) != 20 or len(phase2_questions) != 45:
        raise RuntimeError(f"Totais inesperados: {len(phase2_contests)} concursos e {len(phase2_questions)} questões")
    questions = extend_phase1_questions(base_questions) + phase2_questions
    write_csv(ROOT / "dataset/concursos.csv", CONTEST_FIELDS, base_contests + phase2_contests)
    write_csv(ROOT / "dataset/questoes_discursivas.csv", QUESTION_FIELDS, questions)
    (ROOT / "dados/fase2_pesquisados_nao_incorporados.json").write_text(
        json.dumps(RESEARCHED_NOT_INCLUDED, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"{len(base_contests) + len(phase2_contests)} concursos; {len(questions)} questões; {len(phase2_questions)} novas")


if __name__ == "__main__":
    main()
