# Cadernos TCE-MA — Analista de TI

Projeto de planejamento, execução e acompanhamento dos estudos para o Cargo 10 do concurso do TCE-MA: Analista Estadual de Apoio ao Controle Externo, especialidade Tecnologia da Informação.

## Como retomar o projeto

Ao abrir uma nova sessão de trabalho na raiz deste repositório:

1. Leia `AGENTS.md`; ele contém as regras permanentes do projeto, o escopo do edital e os critérios pedagógicos.
2. Leia `ESTADO.md`; ele informa o que já foi feito, a pendência atual e o próximo passo.
3. Use `documentos de apoio/tce-edital.pdf` como fonte primária. Em caso de conflito, o edital prevalece.
4. Consulte `planos/matriz-prioridade-tce-ma-ti.json` somente depois de considerar erros, revisões vencidas e lacunas individuais.
5. Não presuma desempenho ou domínio que não esteja registrado nos arquivos do projeto.

O histórico da conversa com o assistente não é necessário para retomar o trabalho. As decisões duradouras devem ser registradas no `AGENTS.md`, no `ESTADO.md` ou nos arquivos de resultados.

## Estrutura

- `AGENTS.md`: memória operacional e regras obrigatórias do tutor.
- `ESTADO.md`: ponto de retomada atual.
- `documentos de apoio/tce-edital.pdf`: fonte normativa primária.
- `analises/`: análises de incidência objetiva e da prova discursiva.
- `planos/matriz-prioridade-tce-ma-ti.json`: pesos para distribuição de conteúdo novo.
- `planos/*-plano-executado.json`: entradas históricas usadas pela automação.
- `planos/*-resultados.md`: cadernos criados, URLs e expansões de modalidade ou banca.
- `scripts/tec_cdp.py`: cliente local para comunicação com o Chrome.
- `scripts/tec_create_batch.py`: criação automatizada de cadernos no Tec Concursos.
- `scripts/tec_extract_results.py`: extração do resumo e das questões erradas de cadernos concluídos.

## Requisitos da automação do Tec Concursos

- Python 3.10 ou mais recente. Os scripts usam somente a biblioteca padrão.
- Google Chrome ou Chromium com depuração remota habilitada na porta `9222`.
- Acesso à mesma conta do Tec Concursos usada para criar os cadernos.
- A pasta abaixo já criada na conta do Tec Concursos, com o nome exato:

```text
Analista Estadual de Apoio ao Controle Externo (TCE MA)/2026 - Tecnologia da Informação
```

Cookies, senha e perfil do navegador são dados locais e não devem ser enviados ao GitHub.

### Iniciar o navegador no Linux

Feche instâncias anteriores do perfil de automação e, a partir da raiz do projeto, execute uma das opções abaixo, conforme o navegador instalado:

```bash
google-chrome \
  --remote-debugging-port=9222 \
  '--remote-allow-origins=*' \
  --user-data-dir="$PWD/.chrome-tec-profile" \
  'https://www.tecconcursos.com.br/questoes/cadernos/novo/'
```

ou:

```bash
chromium \
  --remote-debugging-port=9222 \
  '--remote-allow-origins=*' \
  --user-data-dir="$PWD/.chrome-tec-profile" \
  'https://www.tecconcursos.com.br/questoes/cadernos/novo/'
```

Entre manualmente no Tec Concursos nesse navegador. O diretório `.chrome-tec-profile/` está ignorado pelo Git e preserva a sessão apenas na máquina local.

### Confirmar a conexão

```bash
python3 scripts/tec_cdp.py state
```

O comando deve retornar um JSON com o título e a URL da página aberta.

### Criar cadernos

Prepare um plano JSON com uma lista de tarefas neste formato:

```json
[
  {
    "name": "TCE-MA | D02-E01 | Nome do bloco | 10Q",
    "search": "Termo pesquisado no Tec",
    "topic": "Nome exato do assunto no Tec",
    "title_prefix": "Prefixo da disciplina no Tec:",
    "quantity": 10,
    "min_year": 2022,
    "max_year": 2026,
    "fallback_min_year": 2010
  }
]
```

Primeiro valide uma tarefa sem gerar o caderno:

```bash
python3 scripts/tec_create_batch.py caminho/do/plano.json --dry-run --limit 1
```

Depois execute o plano:

```bash
python3 scripts/tec_create_batch.py caminho/do/plano.json
```

Também é possível retomar pela posição da tarefa:

```bash
python3 scripts/tec_create_batch.py caminho/do/plano.json --start 3
```

Antes da execução real, confira o nome, o assunto, a quantidade, a modalidade e o saldo apresentados pelo `--dry-run`. Não execute novamente um arquivo marcado como `plano-executado`.

A automação restringe inicialmente o período a `min_year`–`max_year` quando esses campos são informados. Ela tenta primeiro `CEBRASPE (CESPE)` com questões de múltipla escolha e, se o saldo for insuficiente, troca para Certo ou Errado. Se ainda faltar saldo e houver `fallback_min_year`, inclui anos anteriores um a um e registra `expandedBeforeYear`. Uma eventual ampliação para FGV, FCC ou Cesgranrio ainda deve ser feita ou planejada separadamente, pois o script atual não automatiza essa etapa.

## Registro do estudo

Para extrair resultados de um ou mais cadernos concluídos:

```bash
python3 scripts/tec_extract_results.py ID_DO_CADERNO [OUTRO_ID ...]
```

Depois de resolver cada bateria, informe e registre:

- quantidade de acertos e total de questões;
- questões erradas ou duvidosas;
- confiança 1, 2 ou 3 em cada erro ou dúvida;
- diagnóstico no formato `Regra correta | Conceito confundido | Mecanismo do distrator`;
- data prevista do reteste.

Atualize `ESTADO.md` ao encerrar cada sessão. Não marque um tópico como consolidado sem cumprir os critérios definidos no `AGENTS.md`.

## GitHub e nova máquina

O primeiro envio precisa conter os Markdown, JSON, scripts e o PDF do edital. Arquivos de cache e perfis de navegador são excluídos pelo `.gitignore`.

Em uma máquina nova, use `git clone URL_DO_REPOSITORIO`. Em uma pasta que já seja um clone, use `git pull`. Depois do clone, será necessário iniciar o Chrome com depuração remota e entrar novamente no Tec Concursos.
