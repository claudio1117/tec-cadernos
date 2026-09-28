#!/usr/bin/env python3
"""Incorpora somente as fontes oficiais do TCU 2025/2026 ao manifesto da fase 2.

O script e incremental: preserva os PDFs ja validados, baixa apenas os tres
documentos do TCU e substitui o CNJ 2024 na amostra de 20 concursos. Os PDFs do
CNJ permanecem no repositorio como material pesquisado, mas nao incorporado.
"""

from __future__ import annotations

import json
import re
import subprocess
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVENT = "TCU_25_AUFC"
API = f"https://apis.cebraspe.org.br/cebraspe/eventos/{EVENT}"
CDN = "https://cdn.cebraspe.org.br/concursos/tcu_25_aufc/arquivos/{name}"
FILES = [
    ("editais", "E759D201D30A445B934F33FFDEB14868F911821C8674F7C54D91DCC372FF278A.pdf", "tcu_2025_edital.pdf"),
    ("provas", "C755AC0EC03CD62E8802C6DFF89130043E61CE191AD3673D2A017293C5CFBB6E.pdf", "tcu_2025_discursiva.pdf"),
    ("padroes_resposta", "9DE5A2A09DFA527B96AEDBB3838F7B448A59C7E4A2564F4A5778CA44B8613573.pdf", "tcu_2025_padrao_definitivo.pdf"),
]


def request_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 corpus-research/1.0"})
    with urllib.request.urlopen(req, timeout=60) as response:
        return response.read()


def main() -> None:
    api_data = json.loads(request_bytes(API).decode("utf-8"))
    api_files = {
        item["nomeArquivo"].strip(): item
        for item in (api_data.get("arquivosEdital") or []) + (api_data.get("arquivosGabarito") or [])
    }

    documents = []
    for kind, source_name, target_name in FILES:
        if source_name not in api_files:
            raise RuntimeError(f"Arquivo nao confirmado pela API: {source_name}")
        item = api_files[source_name]
        url = CDN.format(name=urllib.parse.quote(source_name, safe=""))
        target = ROOT / "fontes" / kind / target_name
        if not target.exists():
            content = request_bytes(url)
            if not content.startswith(b"%PDF"):
                raise RuntimeError(f"Conteudo nao e PDF: {url}")
            target.write_bytes(content)
        check = subprocess.run(["pdfinfo", str(target)], capture_output=True, text=True)
        if check.returncode != 0:
            raise RuntimeError(f"PDF invalido: {target}: {check.stderr}")
        match = re.search(r"^Pages:\s+(\d+)", check.stdout, re.MULTILINE)
        if not match:
            raise RuntimeError(f"Numero de paginas nao recuperado: {target}")
        documents.append({
            "tipo": kind,
            "descricao_api": item.get("descricaoArquivo"),
            "nome_api": source_name,
            "url": url,
            "arquivo_local": str(target.relative_to(ROOT)),
            "paginas": int(match.group(1)),
        })

    manifest_path = ROOT / "dados" / "fase2_fontes.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if any(row["identificador_api"] == EVENT for row in manifest):
        raise RuntimeError("TCU_25_AUFC ja esta no manifesto")
    replaced = [row for row in manifest if row["identificador_api"] == "CNJ_24"]
    if len(replaced) != 1:
        raise RuntimeError("Era esperado exatamente um registro CNJ_24 para substituicao")
    manifest = [row for row in manifest if row["identificador_api"] != "CNJ_24"]
    manifest.insert(13, {
        "identificador_api": EVENT,
        "ano_api": api_data.get("eventoAno"),
        "categoria": "A",
        "cargos": api_data.get("eventoCargos") or [],
        "documentos": documents,
    })
    if len(manifest) != 20:
        raise RuntimeError(f"Manifesto deveria ter 20 certames; tem {len(manifest)}")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("TCU_25_AUFC incorporado; CNJ_24 mantido em disco, fora da amostra final")


if __name__ == "__main__":
    main()
