# Discursivas de TI — CESPE/CEBRASPE

## Objetivo

Este projeto constrói uma base histórica verificável de provas discursivas de Tecnologia da Informação aplicadas pelo CESPE/CEBRASPE. A base permitirá analisar padrões históricos de cobrança e comparar os conceitos efetivamente exigidos nas questões com o conteúdo programático do concurso do TCE-MA para o cargo de Analista Estadual de Apoio ao Controle Externo — Especialidade: Tecnologia da Informação.

Esta etapa não faz previsões, não estima probabilidades e não recomenda prioridades de estudo.

## Escopo da pesquisa

- Período inicial: de 2015 ao ano atual.
- Banca: somente CESPE ou CEBRASPE, após confirmação documental.
- Escolaridade: cargos de nível superior.
- Perfis incluídos: Tecnologia da Informação, Análise de Sistemas, Desenvolvimento de Sistemas, Infraestrutura, Segurança da Informação, Ciência ou Engenharia de Dados, Governança de TI, Auditoria de TI e cargos equivalentes.
- Abrangência institucional: tribunais, órgãos de controle e fiscalização, administração fazendária e financeira e demais órgãos públicos.
- Tipo de avaliação: provas efetivamente discursivas; questões objetivas não são tratadas como discursivas.

## Categorias dos concursos

As categorias preservam concursos de diferentes graus de comparabilidade. Nenhum registro das categorias D ou E deve ser descartado automaticamente; pesos e filtros serão aplicados apenas em análises posteriores.

- **A — órgãos de controle e fiscalização:** TCE, TCU, CGU, CGE, controladorias e equivalentes.
- **B — administração fazendária e financeira:** SEFAZ, secretarias de fazenda e órgãos semelhantes.
- **C — Poder Judiciário:** TJ, TRT, TRE, TRF, STJ e equivalentes.
- **D — outros órgãos públicos:** cargos de TI de nível superior não enquadrados nas categorias anteriores.
- **E — baixa comparabilidade:** provas cuja relação com o cargo de Analista de TI do TCE-MA seja baixa.

## Estrutura

```text
dados/
    fase3_auditoria.json
    fase3_validacao.json
    fase2_fontes.json
    fase2_pesquisados_nao_incorporados.json
    fase2_validacao.json
    tce_ma_conteudo_programatico.json
fontes/
    provas/
    padroes_resposta/
    editais/
dataset/
    concursos.csv
    itens_tce_ma_analise.csv
    questoes_discursivas.csv
scripts/
relatorios/
    analise_exploratoria_fase3.md
    auditoria_semantica_fase3.md
    expansao_fase2.md
    validacao_inicial.md
README.md
```

Os documentos baixados são mantidos em `fontes/` conforme seu tipo. Os arquivos em `dataset/` armazenam os registros estruturados. Scripts reprodutíveis ficam em `scripts/`, e os resultados interpretativos, em `relatorios/`. O edital original do TCE-MA deve permanecer no local em que foi encontrado, sem alteração ou movimentação.

## Esquema dos dados

`dataset/concursos.csv` registra os metadados do certame, URLs dos documentos, categoria de comparabilidade e estado de confirmação.

`dataset/questoes_discursivas.csv` preserva o enunciado integral e, quando disponível, o padrão de resposta, além dos campos analíticos de tema e correspondência com o edital do TCE-MA. Campos temáticos nunca substituem os textos originais.

Campos auxiliares adicionados ao esquema mínimo:

- `categoria_comparabilidade`: categoria A, B, C, D ou E;
- `fonte_enunciado` e `fonte_padrao_resposta`: referência documental precisa usada na extração;
- `status_confirmacao`: indica se os dados foram confirmados ou permanecem como `não confirmado`.
- `area_tce_ma`: área ou áreas do edital relacionadas à questão;
- `forma_cobranca`: lista controlada entre `conceitual`, `situação-problema`, `estudo de caso`, `análise técnica`, `aplicação normativa`, `projeto/arquitetura` e `peça técnica`;
- `nivel_abstracao`: nível analítico da resposta exigida;
- campos `exige_*`: indicadores controlados `sim`, `não` ou `não confirmado`;
- `ano_norma_cobrada`: anos explicitamente cobrados, sem inferência de edição;
- `quesitos_avaliados` e `distribuicao_pontos_padrao`: preservação da rubrica e da pontuação recuperável do padrão oficial.

Campos multivalorados devem adotar uma convenção única durante a validação do pipeline, preferencialmente uma lista JSON válida dentro da célula CSV. Campos sem confirmação não devem ser completados por inferência: devem receber `não confirmado` quando aplicável ou permanecer vazios quando a ausência for meramente técnica e estiver explicada em `observacoes`.

## Metodologia de coleta

1. Identificar concursos potencialmente elegíveis no período e classificá-los nas categorias A–E.
2. Confirmar em documentação oficial a banca, o órgão, o cargo, a especialidade e o nível de escolaridade.
3. Priorizar páginas e documentos hospedados em domínios oficiais do CEBRASPE.
4. Localizar, sempre que possível, o edital, o caderno da prova discursiva e o padrão preliminar ou definitivo de resposta.
5. Registrar a URL original de cada documento e guardar uma cópia na pasta correspondente em `fontes/`.
6. Ler o enunciado integral para confirmar que a questão pertence ao cargo e à especialidade informados e para determinar o conteúdo efetivamente cobrado.
7. Extrair o texto documental sem o substituir por resumos ou classificações.
8. Classificar o conteúdo da questão e relacioná-lo ao conteúdo programático do TCE-MA, registrando a justificativa ou eventuais limitações em `observacoes`.
9. Verificar duplicidades por concurso, cargo, especialidade, identificação da questão e conteúdo, inclusive quando o mesmo documento aparecer em URLs diferentes.
10. Registrar lacunas e divergências como `não confirmado`, sem inventar informações.

## Extração documental e classificação analítica

Cada registro deve permitir distinguir duas camadas:

- **Extração documental:** dados reproduzidos dos documentos, como órgão, cargo, enunciado integral, itens exigidos no padrão de resposta, pontuação, limite de linhas e texto do padrão.
- **Classificação analítica:** categoria A–E, tema principal, subtemas, situação-problema, conhecimento geral ou específico e grau de correspondência com o edital do TCE-MA.

Uma classificação deve decorrer da leitura do enunciado e, quando disponível, do padrão de resposta. O título do concurso e a simples coincidência de palavras não são evidência suficiente. Toda classificação incerta deve ser explicitada em `observacoes`.

## Correspondência com o edital do TCE-MA

Para cada questão histórica, a análise deve registrar:

1. se o conceito cobrado está presente no conteúdo programático do TCE-MA;
2. o item ou os itens específicos do edital que sustentam a relação;
3. o grau da correspondência: `direta`, `parcial`, `apenas relacionada` ou `inexistente`.

A correspondência é conceitual, não apenas lexical. O campo `itens_correspondentes_tce_ma` deve apontar para itens identificáveis em `dados/tce_ma_conteudo_programatico.json`, preservando a terminologia original do edital.

## Regras de qualidade

- Confirmar que a banca foi CESPE ou CEBRASPE.
- Confirmar que a questão pertence ao cargo e à especialidade registrados.
- Usar prioritariamente fontes oficiais e conservar suas URLs originais.
- Registrar edital, prova discursiva e padrão de resposta sempre que disponíveis.
- Não inventar dados ausentes; marcar como `não confirmado` o que não puder ser verificado.
- Não classificar a questão somente pelo título do concurso.
- Manter separados texto extraído e classificação produzida pela pesquisa.
- Evitar duplicar provas ou questões publicadas em endereços distintos.
- Não usar questões objetivas como se fossem discursivas.

## Validação inicial do pipeline — concluída

A primeira rodada foi limitada a **três concursos** CESPE/CEBRASPE de nível superior. Para cada um, foram recuperados edital, prova discursiva e padrão definitivo, preenchidos os dois datasets e avaliadas as correspondências com o conteúdo programático do TCE-MA.

Os resultados, documentos usados, lacunas e problemas do processo estão registrados em `relatorios/validacao_inicial.md`. Essa validação foi aprovada antes da expansão.

### Regeneração dos CSVs da validação

Com os nove PDFs da amostra já presentes em `fontes/`, execute:

```bash
python3 scripts/gerar_dataset_validacao.py
```

O script requer `pdftotext` (Poppler), regrava os dois CSVs e interrompe a execução se não encontrar exatamente os padrões definitivos esperados para os três concursos.

## Fase 2 — expansão controlada concluída

A segunda rodada adicionou o teto aprovado de **20 novos concursos**, escolhidos antes da leitura temática: 14 da categoria A, 3 da B e 3 da C. O corpus consolidado contém 23 concursos e 56 componentes discursivos. Todas as discursivas destinadas aos cargos de TI selecionados foram mantidas, inclusive conhecimentos gerais, itens sem correspondência e tecnologias ausentes do edital atual.

Os 20 certames finais têm edital, caderno e padrão de resposta oficiais. O manifesto de fontes e o resultado dos testes ficam em `dados/fase2_fontes.json` e `dados/fase2_validacao.json`; o relatório completo está em `relatorios/expansao_fase2.md`.

### Regeneração e validação do corpus consolidado

Com os PDFs já presentes em `fontes/`, execute:

```bash
python3 scripts/gerar_dataset_fase2.py
python3 scripts/validar_fase2.py
python3 scripts/gerar_relatorio_fase2.py
```

O primeiro script reconstrói em memória os 3 casos da fase 1 e verifica que seus 25 campos originais permanecem inalterados antes de acrescentar a fase 2. O validador confere duplicatas, chaves, JSON, vocabulários controlados, PDFs e ausência de questões objetivas.

Para uma reconstrução documental a partir da API oficial, `scripts/baixar_fontes_fase2.py` contém a seleção final dos 20 certames e os nomes exatos confirmados pela API. Esse passo exige acesso à rede e não é necessário quando o manifesto e os PDFs já estão presentes.

## Fase 3 — auditoria semântica e análise exploratória concluídas

A Fase 3 manteve fechado o corpus de **23 concursos, 56 componentes discursivos e 9 peças técnicas**. Não houve pesquisa, download ou incorporação de concurso. Cada componente foi confrontado com o enunciado integral, o padrão oficial, os quesitos, a classificação temática e os itens do edital do TCE-MA.

A trilha completa está em `dados/fase3_auditoria.json` e sua síntese em `relatorios/auditoria_semantica_fase3.md`. Foram corrigidos somente campos analíticos previamente documentados; enunciados, padrões, URLs e identificadores permaneceram imutáveis. As regras de correspondência usadas foram:

- `direta`: o conceito exigido aparece expressamente ou de modo inequivocamente equivalente no edital atual;
- `parcial`: há cobertura substancial, mas também conteúdo relevante não explicitado, ou norma/tecnologia/versão distinta;
- `apenas relacionada`: existe proximidade temática sem cobertura direta do conhecimento específico;
- `inexistente`: nenhum item cobre adequadamente o conhecimento exigido.

Normas históricas continuam registradas como tais. A continuidade de um processo pode sustentar correspondência parcial, mas não autoriza equiparar uma norma antiga ao ato atual.

`dataset/itens_tce_ma_analise.csv` transforma os 109 registros hierárquicos do edital em unidades analisáveis. As métricas principais adotam o vínculo canônico mais específico: quando uma questão aponta simultaneamente para um item-pai e um descendente, apenas o descendente recebe a ocorrência. Colunas adicionais preservam os vínculos brutos para rastreabilidade.

`relatorios/analise_exploratoria_fase3.md` apresenta somente estatística descritiva da amostra: distribuição temporal e institucional, cobertura das sete áreas, recorrência separada por componente/concurso/ano, formas de cobrança, exigências do comando, peças técnicas e estrutura dos padrões de resposta. Não há ranking preditivo, probabilidade ou recomendação de estudo.

### Reprodução da Fase 3

Partindo do CSV consolidado da Fase 2 e dos PDFs já armazenados:

```bash
python3 scripts/auditar_semantica_fase3.py
python3 scripts/aplicar_correcoes_fase3.py
python3 scripts/auditar_semantica_fase3.py
python3 scripts/gerar_analise_fase3.py
python3 scripts/validar_fase2.py
python3 scripts/validar_fase3.py
```

O primeiro comando documenta as mudanças antes da aplicação. A segunda execução da auditoria confirma que os valores finais estão no CSV. O validador da Fase 3 reconstrói em memória o estado documental da Fase 2 para confirmar a preservação dos campos primários, verifica os 91 PDFs de concurso já existentes em `fontes/`, JSON, chaves estrangeiras, duplicatas e a ausência de questões objetivas.

## Limitações atuais

Os resultados da Fase 3 devem ser lidos com as seguintes limitações:

- a amostra não é aleatória e se limita aos concursos CESPE/CEBRASPE documentalmente confirmados;
- há concentração em órgãos de controle e fiscalização;
- os editais, cargos, tecnologias e normas mudam no período 2015–2026;
- as nove peças técnicas constituem uma amostra pequena;
- questões do mesmo concurso não são observações independentes;
- ausência histórica no corpus não significa impossibilidade de cobrança;
- correspondência conceitual envolve julgamento analítico documentado;
- frequências não devem ser convertidas em previsão ou probabilidade.
