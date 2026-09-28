#!/usr/bin/env python3
"""Organiza IDs explícitos em subpastas do Tec, preservando os cadernos."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from tec_cdp import CDP, active_page, wait_until_loaded


def organize(cdp: CDP, plan: dict, apply: bool) -> dict:
    config = json.dumps({**plan, "apply": apply}, ensure_ascii=False)
    return cdp.evaluate_async(f"""
    (async () => {{
      const cfg = {config};
      const wait = ms => new Promise(resolve => setTimeout(resolve, ms));
      for (let i = 0; i < 100 && !document.querySelector('[ng-click="vm.lineClick(item)"]'); i++) await wait(100);
      const app = document.querySelector('[ng-app]');
      if (!app || !window.angular) throw new Error('Tela de pastas não carregada');
      const svc = angular.element(app).injector().get('tecDadosCadernos');
      const folders = (await svc.listarPastas()).pastas;
      const parent = folders.find(p => String(p.id) === String(cfg.parent_id));
      if (!parent) throw new Error('Pasta principal ausente');
      const inventory = async () => {{
        await svc.listarItens(parent.id, 'nome', 1);
        const items = [];
        for (const item of svc.itens) {{
          if (item.subpasta) {{
            for (const book of await svc.listarItensSubpasta(parent.id, item.id, 'nome'))
              items.push({{id:book.id, name:book.nome, subfolder:item.id}});
          }} else items.push({{id:item.id, name:item.nome, subfolder:null}});
        }}
        if (items.length !== Number(parent.qtdCadernos))
          throw new Error('Inventário incompleto: ' + items.length + ' de ' + parent.qtdCadernos);
        return items;
      }};
      const before = await inventory();
      const ids = cfg.groups.flatMap(g => g.notebook_ids);
      if (new Set(ids.map(String)).size !== ids.length) throw new Error('ID repetido no plano de organização');
      if (new Set(cfg.groups.map(g => g.subfolder)).size !== cfg.groups.length)
        throw new Error('Nome de subpasta repetido');
      for (const id of ids)
        if (!before.some(book => String(book.id) === String(id)))
          throw new Error('Caderno fora da pasta autorizada: ' + id);
      const changes = [];
      const subfolders = parent.subpastas || [];
      for (const group of cfg.groups) {{
        let destination = subfolders.find(p => p.nome === group.subfolder);
        if (!cfg.apply) {{
          changes.push({{subfolder:group.subfolder, id:destination?.id || null, notebooks:group.notebook_ids}});
          continue;
        }}
        if (!destination) {{
          destination = (await svc.criarSubpasta(parent.id, group.subfolder)).subpasta;
          if (!destination?.id) throw new Error('Subpasta não confirmada: ' + group.subfolder);
          subfolders.push(destination);
        }}
        const moving = group.notebook_ids.filter(id =>
          String(before.find(book => String(book.id) === String(id)).subfolder) !== String(destination.id));
        if (moving.length) await svc.moverSelecionados(parent.id, destination.id,
          {{cadernos:moving.map(Number), subpastas:[]}});
        const actual = await svc.listarItensSubpasta(parent.id, destination.id, 'nome');
        for (const id of group.notebook_ids)
          if (!actual.some(book => String(book.id) === String(id)))
            throw new Error('Movimento não confirmado: ' + id);
        changes.push({{subfolder:group.subfolder, id:destination.id, notebooks:group.notebook_ids, moved:moving}});
      }}
      return {{parent:{{id:parent.id,name:parent.nome}}, apply:cfg.apply, before, changes}};
    }})()
    """)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    parser.add_argument("--apply", action="store_true", help="Efetua a organização; padrão somente confere")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text())
    cdp = CDP(active_page())
    try:
        cdp.call("Page.navigate", {"url": f"https://www.tecconcursos.com.br/questoes/pastas/{int(plan['parent_id'])}"})
        wait_until_loaded(cdp)
        result = organize(cdp, plan, args.apply)
        if args.output:
            args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    finally:
        cdp.close()


if __name__ == "__main__":
    main()
