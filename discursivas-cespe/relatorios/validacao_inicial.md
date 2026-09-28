# Validação inicial do pipeline

## Escopo e resultado

Esta validação foi deliberadamente limitada a três concursos CESPE/CEBRASPE, todos de nível superior e classificados na categoria **A — órgãos de controle e fiscalização**. Foram registrados 11 componentes discursivos: oito questões dissertativas e três peças de natureza técnica.

Não há neste relatório previsão, probabilidade, ranking de temas ou recomendação de estudo. As correspondências abaixo indicam apenas relações conceituais entre cobranças históricas e o conteúdo programático do Cargo 10 do TCE-MA.

## Referência do TCE-MA

O arquivo original localizado foi [`docs/tce-edital.pdf`](../docs/tce-edital.pdf), com 77 páginas. O recorte usado é exatamente o **CARGO 10: ANALISTA ESTADUAL DE APOIO AO CONTROLE EXTERNO – ÁREA: APOIO TÉCNICO-ADMINISTRATIVO – ESPECIALIDADE: TECNOLOGIA DA INFORMAÇÃO**.

O título do cargo está na página física 54 do PDF e o conteúdo programático, nas páginas físicas 55 e 56. O arquivo não exibe numeração impressa de página; por isso `pagina_edital` registra a página física do PDF. A extração resultou em 109 itens, distribuídos em sete áreas:

| Área | Itens estruturados |
|---|---:|
| ENGENHARIA DE DADOS | 24 |
| ENGENHARIA DE SOFTWARE | 23 |
| ANÁLISE DE DADOS | 17 |
| INTELIGÊNCIA ARTIFICIAL | 9 |
| ARQUITETURA DE SOFTWARE | 18 |
| GESTÃO E GOVERNANÇA DE TI | 13 |
| CONTRATAÇÕES DE TI | 5 |

O resultado está em [`dados/tce_ma_conteudo_programatico.json`](../dados/tce_ma_conteudo_programatico.json). A terminologia e aparentes inconsistências do edital foram mantidas, inclusive a repetição da numeração “1” em Engenharia de Dados, “Processo interativo e incremental”, “8. DevOps” e “PMBOK 8 ª edição”.

## Concursos selecionados

| ID | Concurso e aplicação | Cargo/especialidade | Motivo da inclusão | Componentes |
|---|---|---|---|---:|
| `tce_rj_2021_ace_ti` | TCE/RJ, 7/2/2021 | Analista de Controle Externo — Tecnologia da Informação | Mesmo tipo de órgão, denominação de analista e questões específicas com interseção clara com dados, segurança e contratação de TI | 4 |
| `tcdf_2024_ace_ti_infra` | TCDF, 17/11/2024 | Auditor de Controle Externo — TI — Microinformática e Infraestrutura | Concurso recente de controle, com ITIL, contratação de TI e peça técnica | 3 |
| `tce_ms_2025_ace_ti` | TCE/MS, 26/10/2025 | Auditor de Controle Externo — Área TI | Concurso recente de controle, com IA, ITIL e contratação de TI aderentes à terminologia atual do TCE-MA | 4 |

Os três cargos e especialidades foram confirmados simultaneamente no edital, no caderno discursivo e no padrão definitivo. Nenhuma questão objetiva foi incluída.

## Documentos utilizados

Todos os documentos foram obtidos do domínio oficial `cdn.cebraspe.org.br`. As URLs originais estão registradas integralmente nos CSVs.

| Concurso | Edital | Prova discursiva | Padrão definitivo |
|---|---|---|---|
| TCE/RJ | [`tce_rj_2020_edital.pdf`](../fontes/editais/tce_rj_2020_edital.pdf) | [`tce_rj_2021_cargo4_discursiva.pdf`](../fontes/provas/tce_rj_2021_cargo4_discursiva.pdf) | [`tce_rj_2021_cargo4_padrao_definitivo.pdf`](../fontes/padroes_resposta/tce_rj_2021_cargo4_padrao_definitivo.pdf) |
| TCDF | [`tcdf_2024_edital.pdf`](../fontes/editais/tcdf_2024_edital.pdf) | [`tcdf_2024_especialidade3_discursiva.pdf`](../fontes/provas/tcdf_2024_especialidade3_discursiva.pdf) | [`tcdf_2024_especialidade3_padrao_definitivo.pdf`](../fontes/padroes_resposta/tcdf_2024_especialidade3_padrao_definitivo.pdf) |
| TCE/MS | [`tce_ms_2025_edital.pdf`](../fontes/editais/tce_ms_2025_edital.pdf) | [`tce_ms_2025_cargo5_discursiva.pdf`](../fontes/provas/tce_ms_2025_cargo5_discursiva.pdf) | [`tce_ms_2025_cargo5_padrao_definitivo.pdf`](../fontes/padroes_resposta/tce_ms_2025_cargo5_padrao_definitivo.pdf) |

## Questões identificadas e correspondências

Os campos de tema, subtema e correspondência são classificações analíticas. O enunciado integral e a seção expositiva do padrão definitivo foram mantidos separadamente em [`dataset/questoes_discursivas.csv`](../dataset/questoes_discursivas.csv).

### TCE/RJ — 2021

| ID | Tipo e tema | Correspondência | Itens do TCE-MA e justificativa |
|---|---|---|---|
| `tce_rj_2021_ace_ti_q1` | Questão, 20 linhas, 20 pontos — recursos contra decisão do TCE/RJ | inexistente | A questão é de conhecimento geral e cobra direito processual de controle externo. Esse conteúdo não integra o programa específico do Cargo 10. |
| `tce_rj_2021_ace_ti_q2` | Questão, 20 linhas, 20 pontos — regras de associação em mineração de dados | direta | `ANÁLISE DE DADOS — 3 Mineração de dados`; `3.3 Técnicas e tarefas de mineração de dados`; `3.5 Regras de associação`. A técnica efetivamente exigida coincide com item nominal e conceitual do edital. |
| `tce_rj_2021_ace_ti_q3` | Questão, 20 linhas, 20 pontos — BYOD e segurança do acesso remoto | parcial | `GESTÃO E GOVERNANÇA DE TI — 10 Cibersegurança e continuidade de negócios`; `ARQUITETURA DE SOFTWARE — 16 Arquitetura de soluções mobile`; `18 Autenticação única`. O programa cobre a base de segurança, mas não explicita BYOD, MDM nem informação classificada. |
| `tce_rj_2021_ace_ti_peca` | Parecer, 50 linhas, 40 pontos — seis achados de contratação de TIC | parcial | Há cobertura direta de gestão, riscos e contratações de TI, mas a questão aplicou IN nº 1/2019 e as Leis nº 8.666/1993 e nº 10.520/2002. O TCE-MA explicita Lei nº 14.133/2021 e IN nº 94/2022. A correspondência é conceitual, não uma equivalência normativa integral. |

### TCDF — 2024

| ID | Tipo e tema | Correspondência | Itens do TCE-MA e justificativa |
|---|---|---|---|
| `tcdf_2024_ace_ti_infra_q1` | Questão, 20 linhas, 10 pontos — gestão de incidentes e problemas | direta | `GESTÃO E GOVERNANÇA DE TI — 3 Gestão de serviços de TI (ITIL v4)`. A questão exige distinguir duas práticas do framework explicitamente previsto. |
| `tcdf_2024_ace_ti_infra_q2` | Questão, 20 linhas, 10 pontos — equipe, fases e DFD no planejamento da contratação | direta | `GESTÃO E GOVERNANÇA DE TI — 6 Contratações de TI no setor público`; `CONTRATAÇÕES DE TI — 1 Gestão de contratação`; `2.2 Instrução Normativa SGD/ME nº 94/2022`. |
| `tcdf_2024_ace_ti_infra_peca` | Informação, 50 linhas, 40 pontos — camadas OSI e TCP/IP | inexistente | O programa do Cargo 10 não lista redes, TCP/IP ou OSI. A presença genérica da palavra “arquitetura” em outros itens não foi tratada como correspondência. |

### TCE/MS — 2025

| ID | Tipo e tema | Correspondência | Itens do TCE-MA e justificativa |
|---|---|---|---|
| `tce_ms_2025_ace_ti_q1` | Questão, 20 linhas, 15 pontos — benefícios, limitações e aplicações de IA no setor público | direta | Abrange `INTELIGÊNCIA ARTIFICIAL — 1, 2, 4, 5 e 6` e conceitos de APIs, microsserviços, interoperabilidade e cloud native em `ARQUITETURA DE SOFTWARE`. O vínculo decorre das abordagens técnicas exigidas, não só da palavra “IA”. |
| `tce_ms_2025_ace_ti_q2` | Questão, 20 linhas, 15 pontos — fiscalização e fases da contratação de TI | direta | `CONTRATAÇÕES DE TI — 1`, `2`, `2.1 Lei nº 14.133/2021` e `2.2 IN nº 94/2022`, além de `GESTÃO E GOVERNANÇA DE TI — 6`. Normas e processo coincidem diretamente. |
| `tce_ms_2025_ace_ti_q3` | Questão, 20 linhas, 15 pontos — problemas, nível de serviço e configuração | direta | `GESTÃO E GOVERNANÇA DE TI — 3 Gestão de serviços de TI (ITIL v4)`. As três práticas cobradas pertencem ao framework explicitamente previsto. |
| `tce_ms_2025_ace_ti_peca` | Parecer, 60 linhas, 55 pontos — inexigibilidade, ETP, análise técnica, pagamento, SLA e aditivo | direta | `CONTRATAÇÕES DE TI — 1, 2.1 e 2.2`; `GESTÃO E GOVERNANÇA DE TI — 1, 3 e 6`; e `ENGENHARIA DE SOFTWARE — 4 Elicitação e gerenciamento de requisitos`. As normas centrais coincidem com as do TCE-MA. |

## Separação entre extração e análise

No CSV de questões:

- `enunciado_integral`, `itens_exigidos`, `texto_padrao_resposta`, pontuação, limite de linhas e referências de página são dados documentais;
- `tema_principal`, `subtemas`, `situacao_problema`, `conhecimento_geral_ou_especifico`, grau de correspondência e itens correspondentes são classificações produzidas nesta pesquisa;
- listas multivaloradas são armazenadas como arrays JSON válidos dentro da célula CSV;
- a seção expositiva integral de cada padrão definitivo foi extraída até o marcador “QUESITOS AVALIADOS”; as tabelas de conceitos e pontuação permanecem integralmente nos PDFs-fonte.

## Dados não confirmados e divergências

Não ficaram campos materiais sem confirmação nos 11 registros. Foram encontradas, porém, as seguintes divergências ou limitações documentais:

1. O cabeçalho da Questão 2 do padrão definitivo do TCE/MS informa aplicação em **25/10/2025**, enquanto o caderno e as demais questões informam **26/10/2025**. O dataset usa 26/10/2025 e registra a divergência em `observacoes`.
2. O edital do TCE-MA não apresenta número de página impresso detectável. As páginas 55–56 registradas no JSON são páginas físicas do PDF.
3. A IN nº 94/2022 aparece como “SGD/SEDGG/ME” em documento do TCDF e como “SGD/ME” no TCE-MA. A diferença de denominação institucional foi preservada; não impede a identidade normativa.
4. A peça do TCE/RJ reflete normas vigentes na aplicação de 2021 que foram posteriormente substituídas. O texto histórico não foi atualizado ou reinterpretado como se cobrasse as normas atuais.
5. As pontuações dos itens de conteúdo não totalizam, isoladamente, o valor nominal de algumas questões porque os editais reservam parcela para apresentação e estrutura textual: 1,00 ponto no TCE/RJ, 0,50 no TCDF e 0,75 no TCE/MS; nas peças, 2,00, 2,00 e 2,75 pontos, respectivamente.

## Problemas observados no processo

- A página pública do CEBRASPE é carregada por JavaScript. Para evitar inferência de nomes de arquivos, a listagem de documentos foi confirmada pela API pública do próprio CEBRASPE e cada URL foi validada pelo download do PDF.
- Nomes de arquivos e identificadores não seguem um padrão único entre concursos; o controle de duplicidade não pode depender apenas do nome do arquivo.
- Extrações por `pdftotext` trazem quebras de linha de diagramação. O script normaliza somente espaços e quebras, preservando palavras, pontuação e conteúdo.
- Uma mesma prova pode conter conhecimento geral e específico. A questão geral do TCE/RJ foi preservada e marcada como tal, em vez de ser descartada ou classificada artificialmente como TI.
- A comparação exige leitura do conceito cobrado. Por isso a peça OSI/TCP-IP foi marcada como inexistente, apesar de o edital conter outros usos da palavra “arquitetura”.

## Reprodutibilidade e verificações

O script [`scripts/gerar_dataset_validacao.py`](../scripts/gerar_dataset_validacao.py) regenera os CSVs a partir das transcrições verificadas e dos padrões definitivos locais. Foram aplicadas as seguintes verificações:

- JSON do TCE-MA sintaticamente válido e com 109 registros;
- três IDs de concurso únicos;
- 11 IDs de questão únicos e todas as chaves estrangeiras presentes em `concursos.csv`;
- listas multivaloradas válidas como JSON;
- todos os documentos locais legíveis como PDF;
- URLs de edital, prova e padrão registradas para todos os três concursos;
- nenhuma ampliação além dos três concursos de validação.

## Encerramento desta etapa

O pipeline inicial está preenchido e documentado. A coleta deve permanecer parada nesses três concursos até a revisão da metodologia e dos resultados.
