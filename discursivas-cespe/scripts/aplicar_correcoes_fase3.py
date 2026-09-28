#!/usr/bin/env python3
"""Aplica ao CSV apenas as correções previamente registradas na auditoria."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "dataset/questoes_discursivas.csv"
AUDIT_PATH = ROOT / "dados/fase3_auditoria.json"
JSON_FIELDS = {
    "subtemas", "itens_correspondentes_tce_ma", "area_tce_ma",
    "forma_cobranca", "ano_norma_cobrada",
}


def decode(field: str, value: str) -> object:
    return json.loads(value) if field in JSON_FIELDS else value


def encode(field: str, value: object) -> str:
    if field in JSON_FIELDS:
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def main() -> None:
    audit = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
    with CSV_PATH.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames
        rows = list(reader)
    assert fieldnames is not None
    by_id = {row["id_questao"]: row for row in rows}

    applied = 0
    already_final = 0
    for component in audit["componentes"]:
        row = by_id[component["id_questao"]]
        for change in component["alteracoes"]:
            field = change["campo"]
            old = change["valor_anterior"]
            new = change["valor_corrigido"]
            current = decode(field, row[field])
            if current == new:
                already_final += 1
                continue
            if current != old:
                raise SystemExit(
                    f"Conflito em {component['id_questao']}/{field}: "
                    f"esperado {old!r} ou {new!r}, encontrado {current!r}"
                )
            row[field] = encode(field, new)
            applied += 1

    with CSV_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps({"correcoes_aplicadas": applied, "ja_aplicadas": already_final}, ensure_ascii=False))


if __name__ == "__main__":
    main()
