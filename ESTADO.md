# Estado atual do projeto

Última atualização: 26/09/2026.

## Situação

Os 60 itens da primeira bateria foram concluídos e corrigidos objetivamente. O resultado foi 35/60 (58,3%): 8/15 (53,3%) nos conhecimentos gerais e 27/45 (60%) nos específicos. Com a ponderação do edital, a bateria representa 62/105 pontos (59,0%), sem equivaler a uma projeção direta da nota oficial devido à proporção diferente entre gerais e específicos.

Nos gerais, os resultados foram: G01-R1 4/5, G02-R1 3/5 e G03-R1 1/5. Os sete erros gerais e os 18 erros específicos estão diagnosticados em `planos/2026-09-22-resultados-parciais.md`. Em 24/09/2026, o aluno decidiu dispensar temporariamente os níveis de confiança e priorizar os assuntos pela concentração objetiva de erros. Nenhum tópico foi classificado como consolidado.

A D02 foi avaliada em 26/09/2026, incluindo os sete cadernos preliminares que o aluno também respondeu. Há 13 cadernos respondidos e dois substitutos sem respostas naquele caderno. As 70 tentativas representam 58 códigos distintos; não somar repetições como questões novas. São 40 códigos sempre acertados, 16 sempre errados e dois com respostas divergentes entre cadernos. Resultados, diagnósticos e datas de reteste estão em `planos/2026-09-26-resultados.md`.

A D03 está criada e auditada: oito cadernos, 60 códigos distintos, todos não resolvidos, com 15 questões gerais e 45 específicas. Não há coincidência com os 58 códigos respondidos extraídos da D02. Resolver somente a subpasta `01 - D03 - 26-09-2026`, dentro da pasta original do concurso (ID `7170166`). Ordem, URLs, filtros e microresumos estão em `planos/2026-09-26-d03.md`.

Na D03, os gerais são Equivalências Lógicas (5), Administração Indireta (5) e Interpretação de Textos (5). Os específicos são COBIT 2019 (15), Modelagem Dimensional (10), Engenharia de Requisitos (5), Microsserviços (5) e IN SGD/ME nº 94/2022 (10, conteúdo novo). Todos usam Cebraspe e anos 2022–2026; COBIT, Dimensional e Microsserviços exigiram certo ou errado. Não houve expansão de período nem de banca. Nenhum tópico foi consolidado.

O código #2789898 (ITAIPU/2024, questão 38) tem gabarito oficial C incompatível com a contagem de objetivos do COBIT. A prova e o gabarito definitivo foram conferidos; não está anulada. Não ensinar a contagem invertida nem tratá-la como erro conceitual confirmado nessa contagem. Ver a ressalva no resultado de 26/09.

## Trabalho concluído nesta sessão

- Confirmado WSL2/Ubuntu 26.04, Python 3.14 e rede NAT, sem Chrome/Chromium Linux instalado. Chrome do Windows iniciado com depuração em perfil exclusivo e conta autenticada.
- Cliente CDP adaptado para usar `scripts/tec_windows_bridge.ps1` no WSL com NAT; testado com extração, organização e criação reais. A conexão direta continua disponível para o Linux Mint. Instruções no `README.md`.
- Extraídos resultados e erros dos cadernos válidos e preliminares da D02. Confiança continua dispensada conforme decisão anterior; as repetições foram identificadas por código e as respostas divergentes não foram presumidas como recuperação.
- Organização aplicada e conferida em quatro subpastas: `01 - D03 - 26-09-2026` (8 cadernos), `90 - D01 - Historico` (8), `91 - D02 - Respondidos` (13) e `99 - Substitutos sem uso - Nao resolver` (2). Total de 31 cadernos; nenhum foi excluído ou teve respostas modificadas. As demais pastas da conta não foram reorganizadas.
- Automação corrigida para ler saldos de zero e uma questão, aguardar atualização assíncrona do filtro, aceitar pasta configurável, registrar expansões e salvar URLs confirmadas por etapa. A retomada foi testada e pulou um caderno existente. Planos históricos com `executado` no nome são bloqueados para criação real.
- D03 validada antes de gerar, criada, movida para a subpasta própria e auditada por gabarito: 60 posições, 60 códigos distintos e 60 não resolvidas. Registros em `planos/2026-09-26-criacao-d03.json`, `planos/2026-09-26-auditoria-d03.json` e `planos/2026-09-26-organizacao-final.json`.
- Plano preservado como `planos/2026-09-26-plano-d03-executado.json`; não executar novamente. Retestes agendados no resultado de 26/09, com referência explícita às datas de correção.

## Trabalho concluído em 24/09/2026

- Em 24/09/2026, o aluno informou que concluiu os cadernos G01-R1, G02-R1 e G03-R1.
- Após novo login feito pelo aluno, os resultados e gabaritos dos três cadernos foram extraídos da conta do Tec Concursos.
- Resultado geral registrado por bloco: G01-R1 4/5, G02-R1 3/5 e G03-R1 1/5; total 8/15.
- Os sete erros gerais foram registrados no formato `Regra correta | Conceito confundido | Mecanismo do distrator`.
- A primeira bateria foi totalizada em 35/60 (58,3%), ou 62/105 (59,0%) com os pesos do edital.
- Por solicitação do aluno, as confianças deixaram de ser requisito para avançar; os retestes foram priorizados pela quantidade e concentração de erros.
- Bateria D02 criada: gerais com 10 questões de Administração Indireta e 5 de Equivalências Lógicas; específicos com 15 de Modelagem Dimensional, 10 de COBIT 2019, 10 de Projeto e Modelagem de Dados, 5 de Engenharia de Requisitos e 5 de Microsserviços.
- Todos os cadernos válidos usam Cebraspe, questões não resolvidas e anos de 2022 a 2026. Modelagem Dimensional e Microsserviços exigiram expansão de múltipla escolha para certo ou errado; não houve expansão de período nem de banca.
- Cadernos separados do mesmo assunto foram auditados quanto a duplicidade. Sete cadernos preliminares com sobreposição foram substituídos e marcados para não resolução em `planos/2026-09-24-retestes-erros.md`; a bateria final foi validada com 60 códigos distintos em 60 posições.
- Os dois planos de criação de 24/09/2026 foram marcados com o sufixo `plano-executado` e não devem ser executados novamente.

## Trabalho concluído anteriormente

- Resultados dos cadernos E01 a E05 extraídos da conta do Tec Concursos.
- Resultado específico registrado por bloco: E01 7/10, E02 7/10, E03 4/10, E04 8/10 e E05 1/5.
- Diagnósticos dos 18 erros registrados no formato `Regra correta | Conceito confundido | Mecanismo do distrator`.
- Regra permanente de recência acrescentada: selecionar primeiro 2022 em diante, inclusive para gerais e específicos; usar anos anteriores apenas se faltar saldo e registrar a expansão.
- Automação atualizada para aceitar `min_year`, `max_year` e `fallback_min_year` e informar eventual ampliação.
- Novos cadernos gerais G01-R1, G02-R1 e G03-R1 criados com Cebraspe, múltipla escolha, não resolvidas, 2022–2026, sem expansão.
- Plano executado preservado em `planos/2026-09-22-plano-gerais-executado.json`; não executar novamente.

## Pendência atual

- Resolver os oito cadernos da D03, seguindo `planos/2026-09-26-d03.md`. Revisões em segmentos de 5; IN 94/2022 em bloco novo de 10.
- Não executar novamente D01/D02 nem resolver a subpasta `99 - Substitutos sem uso - Nao resolver`. O uso dos preliminares foi incorporado ao histórico.
- Ao concluir a D03, extrair os resultados, diagnosticar os erros e agendar seu D+7 pela data real de conclusão/correção, sem exigir confiança por enquanto.

## Próximo passo

1. O aluno lê os microresumos e resolve a bateria D03, mantendo os segmentos indicados no plano.
2. O aluno avisa a conclusão.
3. O tutor lê este estado e `planos/2026-09-26-resultados.md`, extrai a D03 e prepara a próxima rodada priorizando erros e retestes vencidos.
4. Preservar a validação de Projeto e Modelagem de Dados agendada para 29/09, os gerais para 01/10 e os assuntos da correção de 26/09 para 03/10. Integrar os retestes à meta diária; não tratá-los como carga adicional automática.

## Dependências externas

- Os cadernos pertencem à conta do aluno no Tec Concursos; as URLs não substituem a autenticação.
- Em uma nova máquina, é necessário entrar novamente nessa conta.
- Para usar a automação, seguir o `README.md` e manter a pasta de destino do Tec com o nome exato esperado pelo script.
- O caderno incorreto `103891781` permanece em “Cadernos excluídos” e não deve ser restaurado.
