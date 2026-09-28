#!/usr/bin/env python3
"""Extrai o resumo e as questões erradas de cadernos concluídos no Tec."""

from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path

from tec_cdp import CDP, active_page, wait_until_loaded


def open_page(cdp: CDP, url: str) -> None:
    cdp.call("Page.navigate", {"url": url})
    wait_until_loaded(cdp)


def open_answer_key(cdp: CDP) -> None:
    cdp.evaluate_async(
        """
        (async () => {
          const wait = ms => new Promise(resolve => setTimeout(resolve, ms));
          const tab = [...document.querySelectorAll('span.texto-aba')]
            .find(element => element.innerText.trim() === 'Gabarito');
          if (!tab) throw new Error('Aba Gabarito ausente');
          tab.parentElement.click();
          const deadline = Date.now() + 10000;
          while (Date.now() < deadline) {
            const rows = [...document.querySelectorAll('table tbody tr.questao')];
            if (rows.length && rows.every(row =>
              row.querySelector('.num-questao') && row.querySelector('.resultado')
            )) return true;
            await wait(100);
          }
          throw new Error('Gabarito não carregou');
        })()
        """
    )


def read_rows(cdp: CDP) -> list[dict]:
    return cdp.evaluate(
        """
        (() => [...document.querySelectorAll('table tbody tr.questao')]
          .filter(row => row.querySelector('.num-questao'))
          .map(row => {
          const marked = row.querySelector('.alternativa.marcada-certa, .alternativa.marcada-errada');
          const code = row.querySelector('a[href*="/questoes/"]');
          return {
            number: Number(row.querySelector('.num-questao').innerText.trim()),
            code: code ? code.innerText.trim().replace('#', '') : null,
            status: row.querySelector('.resultado').innerText.trim(),
            marked: marked ? marked.innerText.trim() : null
          };
        }))()
        """
    )


def read_error(cdp: CDP, notebook_url: str, number: int, code: str) -> dict:
    open_page(cdp, notebook_url)
    open_answer_key(cdp)
    value = cdp.evaluate_async(
        f"""
        (async () => {{
          const wait = ms => new Promise(resolve => setTimeout(resolve, ms));
          const link = document.querySelector('#questao-{number} .num-questao a');
          if (!link) throw new Error('Questão {number} ausente no gabarito');
          link.click();
          const deadline = Date.now() + 10000;
          while (Date.now() < deadline) {{
            const body = document.body.innerText;
            if (body.includes('Questão {number} de ') &&
                body.includes('#{code} ') && body.includes('Gabarito:')) {{
              return {{body}};
            }}
            await wait(100);
          }}
          throw new Error('Questão {number} não carregou');
        }})()
        """
    )
    body = value["body"]
    correct = re.search(r"Gabarito:\s*([^\.\s]+)", body)
    subject = re.search(r"Assunto:\s*\n([^\n]+)", body)
    header = re.search(r"#(\d+)\s+(.+?)\n", body)
    return {
        "correct": correct.group(1) if correct else None,
        "subject": subject.group(1).strip() if subject else None,
        "header": header.group(2).strip() if header else None,
        "body": body,
    }


def extract_notebook(cdp: CDP, notebook_id: str, summary_only: bool = False) -> dict:
    url = f"https://www.tecconcursos.com.br/questoes/cadernos/{notebook_id}"
    open_page(cdp, url)
    page = cdp.evaluate("({title: document.title})")
    open_answer_key(cdp)
    rows = read_rows(cdp)
    errors = []
    for row in rows:
        if summary_only or "Errou" not in row["status"]:
            continue
        detail = read_error(cdp, url, row["number"], row["code"])
        errors.append({**row, **detail})
    return {
        "id": notebook_id,
        "url": url,
        "title": page["title"],
        "summary": {
            "total": len(rows),
            "answered": sum(row["status"] in {"Acertou", "Errou"} for row in rows),
            "correct": sum(row["status"] == "Acertou" for row in rows),
            "wrong": sum(row["status"] == "Errou" for row in rows),
        },
        "rows": rows,
        "errors": errors,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("notebook_ids", nargs="+")
    parser.add_argument("--summary-only", action="store_true")
    parser.add_argument("--output", type=Path, help="Salva a extração e preserva progresso por caderno")
    args = parser.parse_args()
    cdp = CDP(active_page())
    results = []
    for notebook_id in args.notebook_ids:
        results.append(extract_notebook(cdp, notebook_id, args.summary_only))
        if args.output:
            args.output.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n")
            print(json.dumps({"id": notebook_id, **results[-1]["summary"]}), flush=True)
        time.sleep(0.2)
    if not args.output:
        json.dump(results, fp=__import__("sys").stdout, ensure_ascii=False, indent=2)
    print()
    cdp.close()


if __name__ == "__main__":
    main()
