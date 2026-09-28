# Expansão controlada do corpus — fase 2

## Escopo e resultado

A fase 2 incorporou **20 novos concursos** CESPE/CEBRASPE, atingindo o teto definido. A seleção foi feita por órgão, cargo, nível e existência documental da prova discursiva; os temas cobrados só foram lidos e classificados depois de fechada a elegibilidade. Não houve busca de provas por termos do edital do TCE-MA.

O corpus consolidado contém **23 concursos** e **56 componentes discursivos**. Nesta expansão entraram **45 componentes**, dos quais **6 peças técnicas**. Considerando também a fase 1, há **9 peças técnicas**. Nenhuma questão objetiva foi incluída.

A documentação incorporada soma **88 PDFs oficiais**: 23 editais, 29 cadernos discursivos e 36 padrões de resposta. Há ainda 3 PDFs do CNJ 2024 preservados em `fontes/`, mas não incorporados à amostra final após a substituição pelo TCU 2025/2026. Dos 36 padrões usados no corpus, 31 são definitivos e 5 são preliminares (todos do TCE/PR 2016, única versão oficial localizada).

## Concursos adicionados

| Categoria | Ano da prova | Concurso/cargo de TI | Questões | Peças |
|---|---|---|---|---|
| A | 2026 | Tribunal de Contas do Estado do Rio Grande do Norte (TCE/RN) — Tecnologia da Informação — cargos 4, 5 e 12 | 3 | 0 |
| A | 2026 | Tribunal de Contas do Estado de Minas Gerais (TCE/MG) — Ciência da Computação — cargo 1 | 2 | 0 |
| A | 2025 | Tribunal de Contas do Estado do Rio Grande do Sul (TCE/RS) — Tecnologia da Informação — cargo 4 | 2 | 0 |
| A | 2024 | Tribunal de Contas do Estado do Paraná (TCE/PR) — Informática — cargo 5 | 5 | 1 |
| A | 2024 | Tribunal de Contas do Estado do Acre (TCE/AC) — Gestão de Dados; Infraestrutura de TI; Planejamento de TI; Projetos de TI; Segurança da Informação; Sistemas de Informação — cargos 6 a 11 | 1 | 0 |
| A | 2023 | Tribunal de Contas do Distrito Federal (TCDF) — Tecnologia da Informação – Orientação Sistemas de TI — cargo 3 | 3 | 1 |
| A | 2022 | Tribunal de Contas do Estado de Santa Catarina (TCE/SC) — Ciências da Computação — cargo 3 | 1 | 1 |
| A | 2019 | Tribunal de Contas do Estado de Rondônia (TCE/RO) — Tecnologia da Informação — cargo 1 | 1 | 0 |
| A | 2018 | Tribunal de Contas do Estado de Minas Gerais (TCE/MG) — Ciências da Computação — cargo 4 | 2 | 0 |
| A | 2018 | Controladoria-Geral do Município de João Pessoa (CGM/JP) — Desenvolvimento de Sistemas — cargo 3 | 1 | 0 |
| A | 2016 | Tribunal de Contas do Estado do Paraná (TCE/PR) — Informática — cargo 8 | 5 | 1 |
| A | 2016 | Tribunal de Contas do Estado do Pará (TCE/PA) — Informática — cargos 32 a 36 | 1 | 0 |
| A | 2015 | Tribunal de Contas da União (TCU) — Tecnologia da Informação — cargo 2 | 4 | 1 |
| A | 2026 | Tribunal de Contas da União (TCU) — Orientação: Auditoria de Tecnologia da Informação | 4 | 1 |
| B | 2025 | Secretaria de Estado da Fazenda de Sergipe (SEFAZ/SE) — Tecnologia da Informação — especialidade 2 | 2 | 0 |
| B | 2026 | Secretaria de Estado da Fazenda do Paraná (SEFA/PR) — Profissional de Tecnologia da Informação — cargo 6 | 1 | 0 |
| B | 2021 | Secretaria da Fazenda do Estado do Ceará (SEFAZ/CE) — Tecnologia da Informação da Receita Estadual — cargo 4 | 3 | 0 |
| C | 2024 | Superior Tribunal de Justiça (STJ) — Análise de Sistemas de Informação — cargo 3; Suporte em Tecnologia da Informação — cargo 18 | 2 | 0 |
| C | 2025 | Tribunal Regional do Trabalho da 10.ª Região (TRT10) — Tecnologia da Informação — cargo 11 | 1 | 0 |
| C | 2025 | Tribunal Regional Federal da 6.ª Região (TRF6) — Análise de Dados; Análise de Sistemas de Informação; Governança e Gestão de TI; Tecnologia da Informação — cargos 2, 3, 13 e 22 | 1 | 0 |

Quando um único caderno foi destinado a várias especialidades de TI — TCE/AC 2024, TCE/PA 2016 e TRF6 2025 — o enunciado foi registrado uma vez, e todas as especialidades destinatárias foram preservadas no campo `especialidade`. Isso evita multiplicar artificialmente a mesma questão.

## Documentos utilizados

Todos os 79 documentos da fase 2 que sustentam os 20 concursos finais foram localizados pela API pública do CEBRASPE, recuperados do CDN oficial e validados como PDF. O manifesto `dados/fase2_fontes.json` registra, para cada arquivo, descrição da API, nome oficial, URL, caminho local e número de páginas. Os 9 PDFs da fase 1 foram mantidos sem alteração.

Os campos `texto_padrao_resposta` e `quesitos_avaliados` guardam a extração integral das páginas pertinentes do padrão; `distribuicao_pontos_padrao` preserva o total e os valores explícitos recuperáveis. Classificações analíticas permanecem em campos separados.

## Distribuição por tipo de órgão

| Categoria | Concursos novos | Componentes novos |
|---|---|---|
| A | 14 | 35 |
| B | 3 | 6 |
| C | 3 | 4 |
| D | 0 | 0 |
| E | 0 | 0 |

No corpus total, os 23 concursos distribuem-se em 17 da categoria A, 3 da B e 3 da C. Não foram incluídos concursos D ou E antes de atingir o teto com as prioridades superiores; isso não constitui exclusão temática e não estabelece peso analítico futuro.

## Distribuição por ano de aplicação

| Ano | Componentes novos | Corpus total |
|---|---|---|
| 2015 | 4 | 4 |
| 2016 | 6 | 6 |
| 2018 | 3 | 3 |
| 2019 | 1 | 1 |
| 2021 | 3 | 7 |
| 2022 | 1 | 1 |
| 2023 | 3 | 3 |
| 2024 | 8 | 11 |
| 2025 | 6 | 10 |
| 2026 | 10 | 10 |

O ano registrado é o da aplicação da prova, não necessariamente o ano no identificador do evento. Assim, por exemplo, TCE/SC 2021 aparece como 2022; TCE/MG 2025, SEFA/PR 2025 e TCU 2025 aparecem como 2026; TRT10 2024 e TRF6 2024 aparecem como 2025.

## Correspondência conceitual com o edital do TCE-MA

| Classificação | Novas questões | Corpus total |
|---|---|---|
| direta | 15 | 22 |
| parcial | 15 | 17 |
| apenas relacionada | 4 | 4 |
| inexistente | 11 | 13 |

As correspondências foram feitas após a coleta e pela substância do enunciado e do padrão. Toda correspondência direta ou parcial aponta itens específicos de `dados/tce_ma_conteudo_programatico.json`. Questões gerais e conteúdos ausentes do edital foram mantidos, inclusive as 11 novas classificadas como inexistentes.

## Concursos pesquisados mas não incorporados

| Evento | Situação | Motivo |
|---|---|---|
| CNJ_24 | elegível, não incorporado | Substituído antes da classificação temática pelo TCU_25_AUFC, de prioridade 1 e maior comparabilidade; PDFs oficiais preservados em fontes/. |
| SEFIN_FORTALEZA_CE_23 | elegível, não incorporado | Teto de 20 novos concursos atingido com certames de maior prioridade; discursiva era geral e comum aos analistas. |
| CGE_CE_18 | rejeitado | Cargo de TI identificado, mas sem prova discursiva. |
| CGE_RJ_23 | rejeitado | Cargo genérico de Auditor do Estado; especialidade de TI não confirmada documentalmente. |
| TCE_PE_17 | rejeitado | Não foi localizado cargo superior de TI no certame. |
| TCE_PB_17 | rejeitado | Documentação não confirmou especialidade de TI; referência apenas genérica a demais áreas. |
| SEFAZ_AL_19 / SEFAZ_AL_21 / SEFAZ_RR_21 / SEFAZ_SE_21 / SEFAZ_RN_25 / SEFAZ_RJ_25_AUDITOR | rejeitado | Cargos fiscais genéricos, sem especialidade de TI documentalmente confirmada. |
| SEFAZ_RJ_25_ANALISTA | rejeitado | Especialidades administrativas, contábeis, econômicas e financeiras; não havia cargo de TI. |
| SERPRO_23 / DATAPREV_23 | rejeitado | Cargos de TI presentes, mas a API oficial não disponibilizou caderno discursivo; componente discursivo não confirmado. |

## Controle de qualidade

A validação automatizada terminou com status **aprovado** e sem erros. Foram conferidos:

- unicidade dos 23 concursos e das 56 questões, inclusive pelo hash do enunciado;
- integridade das chaves estrangeiras;
- validade sintática de todos os campos JSON multivalorados;
- vocabulários controlados para correspondência, forma de cobrança e campos booleanos;
- existência, assinatura PDF e número de páginas dos 79 documentos manifestados na fase 2;
- preservação, campo a campo, dos 25 campos originais das 11 questões da fase 1;
- presença de enunciado e padrão de resposta em todos os registros;
- ausência de questões objetivas e de artefatos de páginas de rascunho nos enunciados.

Não há registros incorporados com `status_confirmacao = não confirmado`. Listas vazias em `ano_norma_cobrada` indicam que o ano/edição não foi identificado com segurança na documentação, e não foram preenchidas por suposição.

O resultado detalhado está em `dados/fase2_validacao.json`.

## Problemas e divergências documentais

- O caderno do TCE/SC tem mapa de caracteres defeituoso na extração de texto. O mapeamento foi revertido de forma determinística e conferido visualmente. A grafia literal `NBR2700` existente no caderno foi preservada; não se fez correção silenciosa.
- A API usa os mesmos nomes de arquivo baseados em hash para a prova e o padrão de SEFA/PR 2025 e TCU 2025. As URLs têm diretórios de evento distintos e retornam conteúdos distintos, o que foi confirmado pelos hashes locais.
- Para o TCE/PR 2016, somente padrões preliminares foram localizados na API oficial; os cinco registros indicam expressamente essa limitação.
- Cadernos comuns a múltiplos cargos poderiam gerar duplicatas artificiais; a unidade de registro adotada foi o enunciado efetivamente distinto, com todos os cargos de TI destinatários indicados.
- Alguns identificadores oficiais usam o ano do edital, enquanto a prova ocorreu no ano seguinte. O campo `ano` usa a aplicação e `observacoes` preserva o contexto.

## Limitações

- A amostra foi encerrada ao atingir 20 novos concursos; ela não é um censo de todas as provas entre 2015 e 2026.
- A normalização textual remove espaços e artefatos de leiaute, mas os PDFs originais permanecem disponíveis para conferência.
- Campos como tema, forma de cobrança, nível de abstração e correspondência são classificações analíticas, não trechos documentais.
- `ano_norma_cobrada` fica como lista vazia quando o enunciado não explicita o ano ou a edição; nenhum ano foi presumido.
- Concursos elegíveis de prioridade inferior podem existir fora desta amostra; a coleta foi deliberadamente interrompida no teto aprovado.

## Encerramento da fase

Esta etapa não produz ranking, frequência interpretada, probabilidade, previsão de cobrança ou recomendação de estudo. O corpus fica aguardando revisão metodológica antes de qualquer análise estatística final.
