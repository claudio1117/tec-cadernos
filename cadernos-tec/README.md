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
- `scripts/tec_windows_bridge.ps1`: conexão local com o Chrome do Windows no WSL.
- `scripts/tec_create_batch.py`: criação automatizada de cadernos no Tec Concursos.
- `scripts/tec_extract_results.py`: extração do resumo e das questões erradas de cadernos concluídos.
- `scripts/tec_organize.py`: organização de IDs explícitos em subpastas, com verificação de origem e destino.

## Requisitos da automação do Tec Concursos

- Python 3.10 ou mais recente. Os scripts usam somente a biblioteca padrão.
- Google Chrome ou Chromium com depuração remota habilitada na porta `9222`.
- Acesso à mesma conta do Tec Concursos usada para criar os cadernos.
- A pasta abaixo já criada na conta do Tec Concursos, com o nome exato:

```text
Analista Estadual de Apoio ao Controle Externo (TCE MA)/2026 - Tecnologia da Informação
```

Cookies, senha e perfil do navegador são dados locais e não devem ser enviados ao GitHub.

### Iniciar o navegador no WSL

O Python continua executando no Linux. Para usar o Chrome instalado no Windows, abra um perfil exclusivo pelo PowerShell do Windows:

```powershell
Start-Process -FilePath 'C:\Program Files\Google\Chrome\Application\chrome.exe' -ArgumentList '--remote-debugging-port=9222', '--remote-allow-origins=http://127.0.0.1:9222', "--user-data-dir=$env:LOCALAPPDATA\TecCadernosChrome", 'https://www.tecconcursos.com.br/questoes/cadernos/novo/'
```

Entre na sua conta nesse navegador e execute `python3 scripts/tec_cdp.py state` no WSL. No modo NAT, o cliente detecta que o localhost do Linux não alcança o navegador e usa `tec_windows_bridge.ps1` para conectar ao localhost do Windows. A comunicação passa por entrada e saída padrão do PowerShell, sem modificar firewall nem encaminhar portas. No Linux com navegador local, permanece a conexão direta.

A ponte requer PowerShell do Windows acessível em `/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe` e o comando `wslpath`. Para diagnóstico, `TEC_CDP_TRANSPORT=windows` força a ponte; `TEC_CDP_TRANSPORT=direct` força conexão direta. `TEC_DEBUG_URL` permite alterar o endereço de depuração.

A diferença entre NAT e rede espelhada está documentada pela [Microsoft](https://learn.microsoft.com/windows/wsl/networking). O perfil separado atende à exigência atual do [Chrome para depuração remota](https://developer.chrome.com/blog/remote-debugging-port).

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

Use `--output planos/registro-criacao.json` para preservar os cadernos confirmados a cada etapa. Ao repetir o comando com o mesmo registro, a automação confere nome e quantidade e pula posições já confirmadas. Se uma geração falhar antes de registrar a URL, confira o último caderno na plataforma antes de tentar novamente. Planos cujo nome contém `executado` são bloqueados para criação real.

Cada tarefa pode informar `folder` para escolher uma pasta diferente da pasta padrão. O gerador atual escolhe a pasta principal; para organizar em subpastas depois, prepare um JSON com `parent_id` e `groups`, cada grupo com `subfolder` e `notebook_ids`. Confira com `python3 scripts/tec_organize.py caminho/organizacao.json`; aplique com `--apply --output planos/registro-organizacao.json`. O script só move IDs encontrados dentro da pasta principal informada e verifica sua presença no destino. O registro preserva a localização anterior. Não exclui cadernos nem modifica respostas.

Antes da execução real, confira o nome, o assunto, a quantidade, a modalidade e o saldo apresentados pelo `--dry-run`. Não execute novamente um arquivo marcado como `plano-executado`.

A automação restringe inicialmente o período a `min_year`–`max_year` quando esses campos são informados. Ela tenta primeiro `CEBRASPE (CESPE)` com questões de múltipla escolha e, se o saldo for insuficiente, troca para Certo ou Errado. Se ainda faltar saldo e houver `fallback_min_year`, inclui anos anteriores um a um e registra `expandedBeforeYear`. Uma eventual ampliação para FGV, FCC ou Cesgranrio ainda deve ser feita ou planejada separadamente, pois o script atual não automatiza essa etapa.

## Registro do estudo

Para extrair resultados de um ou mais cadernos concluídos:

```bash
python3 scripts/tec_extract_results.py ID_DO_CADERNO [OUTRO_ID ...]
```

Acrescente `--output planos/extracao.json` para salvar o progresso por caderno. `--summary-only` extrai os resultados e os códigos sem abrir o texto de cada erro. Compare códigos de questão antes de somar cadernos que possam conter repetições; respostas de um caderno não necessariamente aparecem no gabarito de outro caderno que contém a mesma questão.

Depois de resolver cada bateria, informe e registre:

- quantidade de acertos e total de questões;
- questões erradas ou duvidosas;
- confiança 1, 2 ou 3 em cada erro ou dúvida, quando não houver dispensa temporária registrada no estado;
- diagnóstico no formato `Regra correta | Conceito confundido | Mecanismo do distrator`;
- data prevista do reteste.

Atualize `ESTADO.md` ao encerrar cada sessão. Não marque um tópico como consolidado sem cumprir os critérios definidos no `AGENTS.md`.

## GitHub e nova máquina

O primeiro envio precisa conter os Markdown, JSON, scripts e o PDF do edital. Arquivos de cache e perfis de navegador são excluídos pelo `.gitignore`.

Em uma máquina nova, use `git clone URL_DO_REPOSITORIO`. Em uma pasta que já seja um clone, use `git pull`. Depois do clone, será necessário iniciar o Chrome com depuração remota e entrar novamente no Tec Concursos.
