#!/usr/bin/env python3
"""Baixa e valida as fontes oficiais dos 20 certames selecionados na Fase 2.

Os nomes de origem são conferidos contra a API pública do Cebraspe antes do
download. Nenhuma URL de arquivo é presumida sem essa confirmação.
"""

from __future__ import annotations

import json
import re
import subprocess
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
API = "https://apis.cebraspe.org.br/cebraspe/eventos/{event}"
CDN = "https://cdn.cebraspe.org.br/concursos/{event}/arquivos/{name}"


SELECTED = [
    {"event": "TCE_RN_25", "slug": "tce_rn_2026", "category": "A", "files": [
        ("provas", "F9AB2EBB7F247C3E24C68D6486CD675EE2C25859F7C88992156F9E560634D4DE.pdf", "cargo4_discursiva.pdf"),
        ("provas", "E4812F1B53F384FED7E798C663DF4E89AF23E06A9F74410E650CD34D497C083C.pdf", "cargo5_discursiva.pdf"),
        ("provas", "B51E59EEEFF8976480BFD7DD1119016CF48AF3D729EEDE6BC2165149DF0DF0DB.pdf", "cargo12_discursiva.pdf"),
        ("padroes_resposta", "41F4E6F2F5C71FAD25C216A73511072D11BCCE8923A1BEED88F1E1EC4339B6CD.pdf", "cargo4_padrao_definitivo.pdf"),
        ("padroes_resposta", "1BEFA4A254459CBD9B0F2E662F34DA543A810D2054B78FB55ABC21A7416D44C9.pdf", "cargo5_padrao_definitivo.pdf"),
        ("padroes_resposta", "A4A95EA22A5DD7C0CC1A241F29E10BE9D56549296FAE18D5913AA25A2D1B6F18.pdf", "cargo12_padrao_definitivo.pdf"),
    ]},
    {"event": "TCE_MG_25", "slug": "tce_mg_2025", "category": "A", "files": [
        ("provas", "BD2CA7B4C0692568A4CBE06C5D1343C0B822874EF710889E0663F31DAC0B88A7.pdf", "cargo1_discursiva.pdf"),
        ("padroes_resposta", "57A21750DC72DDA4D36B60BAE7302E3CD96D8FBF7F9976BCB559CBF530D90989.pdf", "cargo1_padrao_definitivo.pdf"),
    ]},
    {"event": "TCE_RS_25", "slug": "tce_rs_2025", "category": "A", "files": [
        ("provas", "20A94A6217EB1821BC8B483AB5B58476AC7C0B164D1B9ED0AA352E2EF2EC8017.pdf", "p3_geral_discursiva.pdf"),
        ("provas", "50010D3AA45DE313D7F398190F24FD83D0BD6A9133312104CE2499CF770EC387.pdf", "cargo4_p4_discursiva.pdf"),
        ("padroes_resposta", "240C0EFE7C3BBBF36D674F04D1F7FF8540F69090BC2127AEA9B783B7D4961174.pdf", "p3_geral_padrao_definitivo.pdf"),
        ("padroes_resposta", "248965FA539108F622B4408875D19534A21A101C9B39AB6527B384C57B77E602.pdf", "cargo4_p4_padrao_definitivo.pdf"),
    ]},
    {"event": "TCE_PR_24_AUDITOR", "slug": "tce_pr_2024", "category": "A", "files": [
        ("provas", "TCEPR_CARGO_5_DISC.PDF", "cargo5_discursiva.pdf"),
        ("padroes_resposta", "TCEPR_PADRO_DEFINITIVO_DE_RESPOSTAS_CARGO_5.PDF", "cargo5_padrao_definitivo.pdf"),
    ]},
    {"event": "TCE_AC_24", "slug": "tce_ac_2024", "category": "A", "files": [
        ("provas", "993_TCE_AC_001_DISC.PDF", "cargos1a13_discursiva.pdf"),
        ("padroes_resposta", "PADRO_DEFINITIVO_DE_RESPOSTA___CARGOS_1_A_13.PDF", "cargos1a13_padrao_definitivo.pdf"),
    ]},
    {"event": "TC_DF_23", "slug": "tcdf_2023", "category": "A", "files": [
        ("provas", "897_TCDF_DISC_003.PDF", "cargo3_discursiva.pdf"),
        ("padroes_resposta", "TC_DF_23_PADRO_DE_RESPOSTA_DEFINITIVO_CARGO_03.PDF", "cargo3_padrao_definitivo.pdf"),
    ]},
    {"event": "TCE_SC_21_AUDITOR", "slug": "tce_sc_2021", "category": "A", "files": [
        ("provas", "660_TCESC_003_DISC.PDF", "cargo3_discursiva.pdf"),
        ("padroes_resposta", "TCE_SC_21_AUDITOR_PADRO_DE_RESPOSTA_DEFINITIVO_CARGO_03.PDF", "cargo3_padrao_definitivo.pdf"),
    ]},
    {"event": "TCE_RO_19", "slug": "tce_ro_2019", "category": "A", "files": [
        ("provas", "487_TCERO_DISC_001_01.PDF", "cargo1_discursiva.pdf"),
        ("padroes_resposta", "TCE_RO_19_PADRAO_DE_RESPOSTAS_DEFINITIVO_CARGO_1.PDF", "cargo1_padrao_definitivo.pdf"),
    ]},
    {"event": "TCE_MG_18", "slug": "tce_mg_2018", "category": "A", "files": [
        ("provas", "418_TCEMG_DISC04.PDF", "cargo4_discursiva.pdf"),
        ("padroes_resposta", "TCE_MG_2018_QUESTO_1_TODOS_OS_CARGOS_PADRO_DEFINITIVO.PDF", "questao1_padrao_definitivo.pdf"),
        ("padroes_resposta", "TCE_MG_2018_QUESTO_2_CARGO_4_CIENCIAS_DA_COMPUTACAO_PADRO_DEFINITIVO.PDF", "cargo4_questao2_padrao_definitivo.pdf"),
    ]},
    {"event": "PREF_JP_17_CGM", "slug": "cgm_joao_pessoa_2018", "category": "A", "files": [
        ("provas", "356_PMJPCGM_DISC_003_01.PDF", "cargo3_discursiva.pdf"),
        ("padroes_resposta", "PREF_JP_17_para_o_cargo3_PadraoResposta_definitivo.PDF", "cargo3_padrao_definitivo.pdf"),
    ]},
    {"event": "TCE_PR_16_ANALISTA", "slug": "tce_pr_2016", "category": "A", "files": [
        ("provas", "270TCEPR_DISC_008_01.pdf", "cargo8_discursiva.pdf"),
        ("padroes_resposta", "CARGO8_P3-Questao1.pdf", "cargo8_q1_padrao_preliminar.pdf"),
        ("padroes_resposta", "CARGO8_P3-Questao2.pdf", "cargo8_q2_padrao_preliminar.pdf"),
        ("padroes_resposta", "CARGO8_P3-Questao3.pdf", "cargo8_q3_padrao_preliminar.pdf"),
        ("padroes_resposta", "CARGO8_P3-Questao4.pdf", "cargo8_q4_padrao_preliminar.pdf"),
        ("padroes_resposta", "CARGO8_P4-Parecer.pdf", "cargo8_parecer_padrao_preliminar.pdf"),
    ]},
    {"event": "TCE_PA_16", "slug": "tce_pa_2016", "category": "A", "files": [
        ("provas", "251TCEPA_DISC_001_01.pdf", "cargos1e18a38_discursiva.pdf"),
        ("padroes_resposta", "TCE_PA_PADRAO_DE_RESPOSTA_DEFINITIVO_CARGOS_ 1e18a38.pdf", "cargos1e18a38_padrao_definitivo.pdf"),
    ]},
    {"event": "TCU_15_AUFC", "slug": "tcu_2015", "category": "A", "files": [
        ("provas", "TCUAUFC_DISC_P3.pdf", "p3_comum_discursiva.pdf"),
        ("provas", "TCUAUFC_DISC_P4_CARGO_2.pdf", "cargo2_p4_discursiva.pdf"),
        ("padroes_resposta", "TCU_15_AUFC_PADRAO_DE_RESPOSTAS_DEFINITIVO_P3_QUESTAO_1.pdf", "p3_q1_padrao_definitivo.pdf"),
        ("padroes_resposta", "TCU_15_AUFC_PADRAO_DE_RESPOSTAS_DEFINITIVO_P3_QUESTAO_2.pdf", "p3_q2_padrao_definitivo.pdf"),
        ("padroes_resposta", "TCU_15_AUFC_PADRAO_DE_RESPOSTAS_DEFINITIVO_CARGO_2_P4_QUESTAO.pdf", "cargo2_p4_questao_padrao_definitivo.pdf"),
        ("padroes_resposta", "TCU_15_AUFC_PADRAO_DE_RESPOSTAS_DEFINITIVO_CARGO_2_P4_PECA.pdf", "cargo2_p4_peca_padrao_definitivo.pdf"),
    ]},
    {"event": "SEFAZ_SE_25_AUDITOR", "slug": "sefaz_se_2025", "category": "B", "files": [
        ("provas", "BE30FFF6DADB1B68FC18E2F1EFDD7B68536C4904C66C0B7115CCF31428DFE346.pdf", "especialidade2_q1_discursiva.pdf"),
        ("provas", "743034B9704C1FAC38BD9AFEECFBBF39B97371CCEAA4D281022A5BB5715DC2E2.pdf", "especialidade2_q2_discursiva.pdf"),
        ("padroes_resposta", "FE4406D28028C7E7DAFB48DA595662D2CDE3F66214AB35EAF359248DB5E688F9.pdf", "especialidade2_q1_padrao_definitivo.pdf"),
        ("padroes_resposta", "F912C3E904255E26D7AF109A8D45AE21AC8BDD15C90AC8277791BAAB60F4281E.pdf", "especialidade2_q2_padrao_definitivo.pdf"),
    ]},
    {"event": "SEFA_PR_25", "slug": "sefa_pr_2025", "category": "B", "files": [
        ("provas", "C755AC0EC03CD62E8802C6DFF89130043E61CE191AD3673D2A017293C5CFBB6E.pdf", "discursiva.pdf"),
        ("padroes_resposta", "9DE5A2A09DFA527B96AEDBB3838F7B448A59C7E4A2564F4A5778CA44B8613573.pdf", "padrao_definitivo.pdf"),
    ]},
    {"event": "SEFAZ_CE_21", "slug": "sefaz_ce_2021", "category": "B", "files": [
        ("provas", "598_SEFAZ_004_DISC.PDF", "cargo4_discursiva.pdf"),
        ("padroes_resposta", "SEFAZ_CE_21_PADRO_DE_RESPOSTA_DEFINITIVO_CARGO_4_COMPLETO.PDF", "cargo4_padrao_definitivo.pdf"),
    ]},
    {"event": "STJ_24", "slug": "stj_2024", "category": "C", "files": [
        ("provas", "018_STJ_003_DISC.PDF", "cargo3_discursiva.pdf"),
        ("provas", "018_STJ_018_DISC.PDF", "cargo18_discursiva.pdf"),
        ("padroes_resposta", "PADRO_DEFINITIVO_DE_RESPOSTA___CARGO_3.PDF", "cargo3_padrao_definitivo.pdf"),
        ("padroes_resposta", "PADRO_DEFINITIVO_DE_RESPOSTA___CARGO_18.PDF", "cargo18_padrao_definitivo.pdf"),
    ]},
    {"event": "TRT10_24", "slug": "trt10_2024", "category": "C", "files": [
        ("provas", "050_TRT10_DISC_011.pdf", "cargo11_discursiva.pdf"),
        ("padroes_resposta", "PADRÃO DEFINITIVO DE RESPOSTA_PROVA DISCURSIVA_CARGO 11.pdf", "cargo11_padrao_definitivo.pdf"),
    ]},
    {"event": "TRF6_24", "slug": "trf6_2024", "category": "C", "files": [
        ("provas", "1_PROVA_DISCURSIVA___COMUM_PARA_OS_CARGOS_1_A_7__12__13__19_A_21_E_22.PDF", "cargos_superiores_comum_discursiva.pdf"),
        ("padroes_resposta", "PADRO_DE_RESPOSTA_DEFINITIVO___COMUM_PARA_OS_CARGOS_1_A_7__12__13__19_A_21_E_22.PDF", "cargos_superiores_comum_padrao_definitivo.pdf"),
    ]},
    {"event": "TCU_25_AUFC", "slug": "tcu_2025", "category": "A", "files": [
        ("provas", "C755AC0EC03CD62E8802C6DFF89130043E61CE191AD3673D2A017293C5CFBB6E.pdf", "discursiva.pdf"),
        ("padroes_resposta", "9DE5A2A09DFA527B96AEDBB3838F7B448A59C7E4A2564F4A5778CA44B8613573.pdf", "padrao_definitivo.pdf"),
    ]},
]


def normalize_name(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().casefold()


def request_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 corpus-research/1.0"})
    with urllib.request.urlopen(req, timeout=60) as response:
        return response.read()


def main() -> None:
    manifest: list[dict[str, object]] = []
    for selection in SELECTED:
        event = selection["event"]
        data = json.loads(request_bytes(API.format(event=event)).decode("utf-8"))
        all_files = (data.get("arquivosEdital") or []) + (data.get("arquivosGabarito") or [])
        by_normalized = {normalize_name(item["nomeArquivo"]): item for item in all_files}

        edital_candidates = [
            item for item in (data.get("arquivosEdital") or [])
            if item.get("nomeArquivo", "").lower().endswith(".pdf")
            and "abertura" in item.get("descricaoArquivo", "").casefold()
        ]
        if not edital_candidates:
            raise RuntimeError(f"Edital de abertura não localizado na API: {event}")
        edital_candidates.sort(key=lambda item: "atualiz" not in item.get("descricaoArquivo", "").casefold())
        edital = edital_candidates[0]
        documents = [("editais", edital["nomeArquivo"], "edital.pdf")]
        documents.extend(selection["files"])

        event_docs = []
        for kind, source_name, target_suffix in documents:
            normalized = normalize_name(source_name)
            if normalized not in by_normalized:
                raise RuntimeError(f"Arquivo não confirmado na API {event}: {source_name!r}")
            api_item = by_normalized[normalized]
            actual_name = api_item["nomeArquivo"].strip()
            quoted = urllib.parse.quote(actual_name, safe="")
            url = CDN.format(event=event.lower(), name=quoted)
            target = ROOT / "fontes" / kind / f"{selection['slug']}_{target_suffix}"
            content = request_bytes(url)
            if not content.startswith(b"%PDF"):
                raise RuntimeError(f"Conteúdo não é PDF: {url}")
            target.write_bytes(content)
            check = subprocess.run(["pdfinfo", str(target)], capture_output=True, text=True)
            if check.returncode != 0:
                raise RuntimeError(f"PDF inválido: {target}: {check.stderr}")
            pages = int(re.search(r"^Pages:\s+(\d+)", check.stdout, re.MULTILINE).group(1))
            event_docs.append({
                "tipo": kind,
                "descricao_api": api_item.get("descricaoArquivo"),
                "nome_api": actual_name,
                "url": url,
                "arquivo_local": str(target.relative_to(ROOT)),
                "paginas": pages,
            })
        manifest.append({
            "identificador_api": event,
            "ano_api": data.get("eventoAno"),
            "categoria": selection["category"],
            "cargos": data.get("eventoCargos") or [],
            "documentos": event_docs,
        })

    out = ROOT / "dados/fase2_fontes.json"
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(manifest)} certames; {sum(len(x['documentos']) for x in manifest)} PDFs validados")


if __name__ == "__main__":
    main()
