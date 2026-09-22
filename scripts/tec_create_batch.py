#!/usr/bin/env python3
"""Cria uma sequência de cadernos no Tec Concursos via Chrome/CDP."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from tec_cdp import CDP, active_page, wait_until_loaded


FILTER_URL = "https://www.tecconcursos.com.br/questoes/cadernos/novo/"
TARGET_FOLDER = (
    "Analista Estadual de Apoio ao Controle Externo (TCE MA)/2026 - "
    "Tecnologia da Informação"
)


def configure_notebook(cdp: CDP, task: dict) -> dict:
    config = {
        **task,
        "bank": "CEBRASPE (CESPE)",
        "folder": TARGET_FOLDER,
    }
    config_json = json.dumps(config, ensure_ascii=False)
    expression = f"""
    (async () => {{
      const cfg = {config_json};
      const wait = ms => new Promise(resolve => setTimeout(resolve, ms));
      const visible = element => element && element.offsetParent !== null;
      const waitFor = async (fn, label, timeout = 15000) => {{
        const deadline = Date.now() + timeout;
        while (Date.now() < deadline) {{
          const value = fn();
          if (value) return value;
          await wait(100);
        }}
        throw new Error('Timeout: ' + label);
      }};
      const clickMenu = async title => {{
        const item = [...document.querySelectorAll('li.menu-alternador-opcao[title]')]
          .find(element => element.title === title);
        if (!item) throw new Error('Menu ausente: ' + title);
        item.click();
        await waitFor(
          () => [...document.querySelectorAll('li.menu-alternador-opcao.ativa')]
            .some(element => element.title === title),
          'ativar ' + title
        );
        await wait(250);
      }};
      const search = async query => {{
        let input = [...document.querySelectorAll('input[name=campoPesquisa]')].find(visible);
        if (!input) {{
          const link = [...document.querySelectorAll('a.link-limpo')]
            .find(element => visible(element) && element.innerText.trim() === 'Pesquisar por nome');
          if (!link) throw new Error('Busca por nome indisponível');
          link.click();
          input = await waitFor(
            () => [...document.querySelectorAll('input[name=campoPesquisa]')].find(visible),
            'abrir pesquisa'
          );
        }}
        const header = input.closest('.gerador-buscador-cabecalho');
        const vm = angular.element(header).isolateScope().vm;
        vm.textoBusca = query;
        vm.alterarTextoBusca(query);
        await wait(750);
      }};
      const selectTreeItem = async (text, titlePrefix = '') => {{
        const item = await waitFor(() =>
          [...document.querySelectorAll('li.arvore-item')].find(element =>
            visible(element) &&
            element.innerText.trim() === text &&
            (!titlePrefix || element.title.startsWith(titlePrefix))
          ), 'localizar ' + text);
        item.querySelector('.arvore-item-conteudo').click();
        await wait(450);
      }};
      const selectOption = async label => {{
        const item = await waitFor(() =>
          [...document.querySelectorAll('li.arvore-item')].find(element =>
            visible(element) && element.innerText.trim().endsWith(label)
          ), 'opção ' + label);
        if (!item.classList.contains('arvore-item-selecionado')) {{
          item.querySelector('.arvore-item-conteudo').click();
          await wait(350);
        }}
      }};
      const selectYear = async year => {{
        const item = await waitFor(() =>
          [...document.querySelectorAll('li.arvore-item')].find(element =>
            visible(element) && element.innerText.trim() === String(year)
          ), 'ano ' + year);
        if (!item.classList.contains('arvore-item-selecionado')) {{
          item.querySelector('.arvore-item-conteudo').click();
          await wait(250);
        }}
      }};
      const availableCount = () => {{
        const canvas = [...document.querySelectorAll('.gerador-conteudo-canvas-grid')].find(visible);
        if (canvas) {{
          const scope = angular.element(canvas).isolateScope();
          const value = scope && scope.vm && scope.vm.numeroQuestoesEncontradas;
          if (Number.isFinite(Number(value))) return Number(value);
        }}
        const lines = document.body.innerText.split(String.fromCharCode(10)).map(line => line.trim());
        const countLine = lines.find(line => /questões encontradas$/.test(line));
        if (countLine) {{
          const amount = Number(countLine.replace(/[^0-9]/g, ''));
          if (Number.isFinite(amount)) return amount;
        }}
        return null;
      }};

      await waitFor(() => window.angular && document.querySelector('li.menu-alternador-opcao'), 'carregar gerador');
      await clickMenu('Banca');
      await search('CEBRASPE');
      await selectTreeItem(cfg.bank);

      await clickMenu('Matéria e assunto');
      await search(cfg.search);
      await selectTreeItem(cfg.topic, cfg.title_prefix);

      const selectedYears = [];
      if (cfg.min_year && cfg.max_year) {{
        await clickMenu('Ano');
        for (let year = cfg.max_year; year >= cfg.min_year; year--) {{
          await selectYear(year);
          selectedYears.push(year);
        }}
      }}

      await clickMenu('Opções');
      await selectOption('Múltipla escolha');
      await selectOption('Remover as que resolvi');
      await selectOption('Remover anuladas');
      await selectOption('Remover desatualizadas');
      await wait(700);

      let format = 'Múltipla escolha';
      let available = availableCount();
      if (available < cfg.quantity) {{
        const multipleChoice = [...document.querySelectorAll('li.arvore-item')].find(element =>
          visible(element) && element.innerText.trim().endsWith('Múltipla escolha')
        );
        multipleChoice.querySelector('.arvore-item-conteudo').click();
        await wait(250);
        await selectOption('Certo ou Errado');
        format = 'Certo ou Errado';
        await wait(700);
        available = availableCount();
      }}
      let expandedBeforeYear = null;
      if (available < cfg.quantity && cfg.min_year && cfg.fallback_min_year) {{
        await clickMenu('Ano');
        for (let year = cfg.min_year - 1; year >= cfg.fallback_min_year; year--) {{
          await selectYear(year);
          selectedYears.push(year);
          await wait(500);
          available = availableCount();
          expandedBeforeYear = year;
          if (available >= cfg.quantity) break;
        }}
        await clickMenu('Opções');
        await wait(350);
        available = availableCount();
      }}
      if (available < cfg.quantity) {{
        throw new Error('Saldo insuficiente: ' + available + ' para ' + cfg.quantity);
      }}

      const edit = [...document.querySelectorAll('a')]
        .find(element => visible(element) && element.innerText.trim().startsWith('Editar quantidade'));
      if (!edit) throw new Error('Configuração de quantidade indisponível');
      edit.click();
      const totalInput = await waitFor(
        () => [...document.querySelectorAll('input[name=novoTotal]')].find(visible),
        'campo de quantidade'
      );
      const quantityComponent = totalInput.closest('.gerador-configurar-caderno');
      const quantityElement = angular.element(quantityComponent);
      const quantityScope = quantityElement.isolateScope() || quantityElement.scope();
      await wait(700);
      for (let attempt = 0; attempt < 4; attempt++) {{
        quantityScope.$apply(() => {{
          quantityScope.vm.totalQuestoesSelecionadas = cfg.quantity;
          quantityScope.vm.redistribuirProporcionalmente();
        }});
        await wait(500);
        const configured = [...document.querySelectorAll('input[name="materias[].numeroQuestoesCaderno"]')]
          .filter(visible).reduce((sum, input) => sum + Number(input.value || 0), 0);
        if (configured === cfg.quantity) break;
      }}
      await waitFor(() =>
        [...document.querySelectorAll('input[name="materias[].numeroQuestoesCaderno"]')]
          .filter(visible).reduce((sum, input) => sum + Number(input.value || 0), 0) === cfg.quantity,
        'redistribuir quantidade'
      );

      const nameInput = [...document.querySelectorAll('#nomeCadernoId')].find(visible);
      const folder = [...document.querySelectorAll('#pastaCadernosId')].find(visible);
      const notebookComponent = nameInput.closest('.gerador-caderno');
      const notebookElement = angular.element(notebookComponent);
      const notebookScope = notebookElement.isolateScope() || notebookElement.scope();
      const destination = notebookScope.vm.pastasCadernos.find(item => item.nome === cfg.folder);
      if (!destination) throw new Error('Pasta de destino ausente');
      notebookScope.$apply(() => {{
        notebookScope.vm.nomeCaderno = cfg.name;
        notebookScope.vm.pastaCadernosAtual = destination;
      }});
      await waitFor(() => nameInput.value === cfg.name, 'confirmar nome');
      await waitFor(() => folder.selectedOptions[0].text === cfg.folder, 'confirmar pasta');

      const generate = [...document.querySelectorAll('button')]
        .find(element => visible(element) && element.innerText.trim().toUpperCase() === 'GERAR CADERNO');
      if (!generate || generate.disabled) throw new Error('Botão Gerar Caderno indisponível');
      return {{
        name: nameInput.value,
        folder: folder.selectedOptions[0].text,
        requested: cfg.quantity,
        totalModel: quantityScope.vm.totalQuestoesSelecionadas,
        nameModel: notebookScope.vm.nomeCaderno,
        available,
        format,
        selectedYears,
        expandedBeforeYear,
        topic: cfg.topic,
        generateReady: !generate.disabled
      }};
    }})()
    """
    value = cdp.evaluate_async(expression)
    return value if isinstance(value, dict) else json.loads(value)


def generate_notebook(cdp: CDP, expected_quantity: int) -> dict:
    clicked = cdp.evaluate("""
      (() => {
        const button = [...document.querySelectorAll('button')]
          .find(element => element.innerText.trim().toUpperCase() === 'GERAR CADERNO');
        if (!button || button.disabled) throw new Error('Botão Gerar Caderno indisponível');
        button.click();
        return true;
      })()
    """)
    if not clicked:
        raise RuntimeError("O clique para gerar o caderno falhou")

    deadline = time.monotonic() + 30
    while time.monotonic() < deadline:
        try:
            state = cdp.evaluate("""
              (() => {
                const text = document.body ? document.body.innerText : '';
                return JSON.stringify({
                  url: location.href,
                  title: document.title,
                  position: (text.match(/\\b1 de \\d+\\b/) || [null])[0]
                });
              })()
            """)
            state = state if isinstance(state, dict) else json.loads(state)
            if "/questoes/cadernos/" in state["url"] and state["position"]:
                if state["position"] != f"1 de {expected_quantity}":
                    raise RuntimeError(f"Quantidade criada inesperada: {state['position']}")
                return state
        except (ConnectionError, json.JSONDecodeError):
            pass
        time.sleep(0.25)
    raise TimeoutError("O caderno não foi confirmado após a geração")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    tasks = json.loads(args.plan.read_text())
    tasks = tasks[args.start - 1 :]
    if args.limit is not None:
        tasks = tasks[: args.limit]

    cdp = CDP(active_page())
    results = []
    for index, task in enumerate(tasks, start=1):
        cdp.call("Page.navigate", {"url": FILTER_URL})
        wait_until_loaded(cdp)
        preflight = configure_notebook(cdp, task)
        if args.dry_run:
            print(json.dumps({"index": index, **preflight}, ensure_ascii=False), flush=True)
            continue
        created = generate_notebook(cdp, task["quantity"])
        result = {"index": index, **preflight, **created}
        results.append(result)
        print(json.dumps(result, ensure_ascii=False), flush=True)

    print(json.dumps({"created": len(results), "results": results}, ensure_ascii=False))


if __name__ == "__main__":
    main()
