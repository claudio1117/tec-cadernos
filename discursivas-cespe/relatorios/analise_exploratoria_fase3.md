# Análise exploratória descritiva — Fase 3

> Escopo fechado: os resultados descrevem exclusivamente o corpus de 23 concursos e 56 componentes confirmado nas fases anteriores. Frequência histórica, cobertura e recência nesta amostra não representam probabilidade de cobrança futura.

## 3.1 — Visão geral

O corpus reúne **23 concursos**, **56 componentes discursivos**, dos quais **47 questões/estudos de caso** e **9 peças técnicas**, no período de **2015 a 2026**.

### Distribuição por ano

| Ano | Concursos distintos | Componentes | Percentual dos componentes |
|---:|---:|---:|---:|
| 2015 | 1 | 4 | 7,1% |
| 2016 | 2 | 6 | 10,7% |
| 2018 | 2 | 3 | 5,4% |
| 2019 | 1 | 1 | 1,8% |
| 2021 | 2 | 7 | 12,5% |
| 2022 | 1 | 1 | 1,8% |
| 2023 | 1 | 3 | 5,4% |
| 2024 | 4 | 11 | 19,6% |
| 2025 | 5 | 10 | 17,9% |
| 2026 | 4 | 10 | 17,9% |

### Distribuição por categoria de órgão

| Categoria | Concursos | Componentes | Percentual dos componentes |
|---|---:|---:|---:|
| A | 17 | 46 | 82,1% |
| B | 3 | 6 | 10,7% |
| C | 3 | 4 | 7,1% |
| D | 0 | 0 | 0,0% |
| E | 0 | 0 | 0,0% |

### Conhecimento geral ou específico

| Natureza | Componentes | Percentual |
|---|---:|---:|
| geral | 13 | 23,2% |
| específico | 43 | 76,8% |

As 13 questões gerais foram mantidas porque integraram a avaliação dos cargos selecionados; elas não foram reclassificadas como técnicas apenas por terem sido aplicadas a candidatos de TI.

### Correspondência com o edital do TCE-MA

| Correspondência | Componentes | Percentual |
|---|---:|---:|
| direta | 20 | 35,7% |
| parcial | 19 | 33,9% |
| apenas relacionada | 4 | 7,1% |
| inexistente | 13 | 23,2% |

## 3.2 — Cobertura das grandes áreas do Cargo 10

A classificação é multirrótulo: um componente pode pertencer a mais de uma área. Portanto, as linhas não devem ser somadas como se representassem componentes independentes.

| Área | Componentes relacionados | Concursos distintos | Anos distintos | Diretas | Parciais | Peças técnicas | Questões não-peça |
|---|---:|---:|---:|---:|---:|---:|---:|
| ENGENHARIA DE DADOS | 5 | 5 | 4 | 2 | 2 | 0 | 5 |
| ENGENHARIA DE SOFTWARE | 12 | 9 | 7 | 3 | 8 | 2 | 10 |
| ANÁLISE DE DADOS | 3 | 2 | 2 | 2 | 1 | 0 | 3 |
| INTELIGÊNCIA ARTIFICIAL | 5 | 5 | 4 | 5 | 0 | 0 | 5 |
| ARQUITETURA DE SOFTWARE | 2 | 2 | 2 | 1 | 1 | 0 | 2 |
| GESTÃO E GOVERNANÇA DE TI | 31 | 18 | 10 | 13 | 15 | 8 | 23 |
| CONTRATAÇÕES DE TI | 7 | 6 | 5 | 5 | 2 | 5 | 2 |

## 3.3 — Itens do edital

As métricas principais usam associação canônica no item mais específico disponível. Se uma questão foi vinculada simultaneamente a um pai e a um descendente, o pai preserva o vínculo registrado, mas não recebe uma segunda ocorrência canônica. As listas A–C consideram a existência do vínculo bruto; as colunas de ocorrência, concurso e ano usam somente a associação canônica. Assim se identifica toda a hierarquia sem transformar uma única cobrança em várias ocorrências do mesmo ramo.

- **39 itens** possuem ao menos uma correspondência direta;
- **13 itens** possuem correspondência parcial, mas nenhuma direta;
- **5 itens** aparecem somente como relacionados;
- **52 itens** não tiveram correspondência nos 56 componentes analisados.

### A) Itens com correspondência direta

| ID | Área | Item | Vínculos diretos | Ocorrências diretas canônicas | Concursos (todas as classes canônicas) | Anos (todas as classes canônicas) |
|---|---|---|---:|---:|---:|---:|
| TCE-MA-004 | ENGENHARIA DE DADOS | 1.3 Coleta, tratamento, armazenamento, integração e recuperação de dados. | 1 | 1 | 2 | 2 |
| TCE-MA-009 | ENGENHARIA DE DADOS | 1.4 Modelagem e normalização de dados. | 1 | 1 | 1 | 1 |
| TCE-MA-012 | ENGENHARIA DE DADOS | 2 Modelagem de dados (conceitual, lógica e física). | 1 | 1 | 1 | 1 |
| TCE-MA-015 | ENGENHARIA DE DADOS | 5 Integridade referencial. | 1 | 1 | 1 | 1 |
| TCE-MA-020 | ENGENHARIA DE DADOS | 10 Administração de banco de dados. | 1 | 0 | 0 | 0 |
| TCE-MA-022 | ENGENHARIA DE DADOS | 10.2 Arquitetura e políticas de armazenamento de dados. | 1 | 1 | 1 | 1 |
| TCE-MA-023 | ENGENHARIA DE DADOS | 10.3 Noções de otimização de performance em larga escala. | 1 | 1 | 1 | 1 |
| TCE-MA-024 | ENGENHARIA DE DADOS | 11 Técnicas de integração e ingestão de dados (ETL/ELT, transferência de arquivos, integração via base de dados). | 1 | 1 | 2 | 2 |
| TCE-MA-027 | ENGENHARIA DE SOFTWARE | 3 Práticas ágeis de desenvolvimento de software. | 1 | 1 | 5 | 5 |
| TCE-MA-028 | ENGENHARIA DE SOFTWARE | 4 Elicitação e gerenciamento de requisitos. | 1 | 1 | 2 | 2 |
| TCE-MA-035 | ENGENHARIA DE SOFTWARE | 5 Práticas ágeis. | 1 | 0 | 0 | 0 |
| TCE-MA-037 | ENGENHARIA DE SOFTWARE | 5.2 Gerenciamento de produtos com métodos ágeis: Scrum e Kanban. | 1 | 1 | 5 | 5 |
| TCE-MA-046 | ENGENHARIA DE SOFTWARE | 8.3 Docker e orquestração com Kubernetes. | 1 | 1 | 1 | 1 |
| TCE-MA-050 | ANÁLISE DE DADOS | 3 Mineração de dados. | 1 | 0 | 0 | 0 |
| TCE-MA-052 | ANÁLISE DE DADOS | 3.2 Técnicas para pré‐processamento de dados. | 1 | 1 | 1 | 1 |
| TCE-MA-053 | ANÁLISE DE DADOS | 3.3 Técnicas e tarefas de mineração de dados. | 2 | 2 | 2 | 2 |
| TCE-MA-054 | ANÁLISE DE DADOS | 3.4 Classificação. | 1 | 1 | 1 | 1 |
| TCE-MA-055 | ANÁLISE DE DADOS | 3.5 Regras de associação. | 1 | 1 | 1 | 1 |
| TCE-MA-058 | ANÁLISE DE DADOS | 3.8 Modelagem preditiva. | 1 | 1 | 1 | 1 |
| TCE-MA-065 | INTELIGÊNCIA ARTIFICIAL | 1 Inteligência artificial: fundamentos e aplicações. | 2 | 2 | 2 | 2 |
| TCE-MA-066 | INTELIGÊNCIA ARTIFICIAL | 2 Aprendizado de máquina. | 3 | 3 | 3 | 2 |
| TCE-MA-067 | INTELIGÊNCIA ARTIFICIAL | 3 IA generativa. | 1 | 1 | 1 | 1 |
| TCE-MA-068 | INTELIGÊNCIA ARTIFICIAL | 4 Redes Neurais e Deep Learning. Arquiteturas de redes neurais, Frameworks, técnicas de treinamento e aplicações. | 2 | 2 | 2 | 2 |
| TCE-MA-069 | INTELIGÊNCIA ARTIFICIAL | 5 Processamento de linguagem natural. Modelos, pré‐processamento, agentes inteligentes e sistemas multiagentes. | 2 | 2 | 2 | 2 |
| TCE-MA-070 | INTELIGÊNCIA ARTIFICIAL | 6 Arquitetura e engenharia de sistemas de IA. MLOps. Deploy de modelos. Integração com computação em nuvem. | 2 | 2 | 2 | 2 |
| TCE-MA-076 | ARQUITETURA DE SOFTWARE | 3 Sistemas de N camadas; microsserviço. | 1 | 1 | 1 | 1 |
| TCE-MA-078 | ARQUITETURA DE SOFTWARE | 5 APIs, arquitetura cloud native. | 1 | 1 | 1 | 1 |
| TCE-MA-081 | ARQUITETURA DE SOFTWARE | 8 Barramento de serviços corporativos (ESB); interoperabilidade entre aplicações. | 1 | 1 | 1 | 1 |
| TCE-MA-092 | GESTÃO E GOVERNANÇA DE TI | 1 Governança corporativa de TI (COBIT 2019, ISO/IEC 38500). | 2 | 2 | 5 | 5 |
| TCE-MA-094 | GESTÃO E GOVERNANÇA DE TI | 3 Gestão de serviços de TI (ITIL v4). | 3 | 3 | 3 | 3 |
| TCE-MA-095 | GESTÃO E GOVERNANÇA DE TI | 4 Gestão de projetos e metodologias ágeis (PMBOK 8 ª edição, SCRUM, Kanban). | 1 | 1 | 5 | 5 |
| TCE-MA-097 | GESTÃO E GOVERNANÇA DE TI | 6 Contratações de TI no setor público. | 5 | 5 | 6 | 5 |
| TCE-MA-101 | GESTÃO E GOVERNANÇA DE TI | 10 Cibersegurança e continuidade de negócios (ISO 27001/22301, 27002, NIST). | 3 | 3 | 11 | 9 |
| TCE-MA-103 | GESTÃO E GOVERNANÇA DE TI | 12 Lei Geral de Proteção de Dados Pessoais (LGPD – Lei nº 13.709/2018). | 2 | 2 | 2 | 2 |
| TCE-MA-105 | CONTRATAÇÕES DE TI | 1 Gestão de contratação de soluções de TI. | 5 | 5 | 6 | 5 |
| TCE-MA-106 | CONTRATAÇÕES DE TI | 2 Legislação aplicável à contratação de bens e serviços de TI e suas alterações. | 3 | 0 | 2 | 2 |
| TCE-MA-107 | CONTRATAÇÕES DE TI | 2.1 Lei nº 14.133/2021. | 4 | 4 | 3 | 3 |
| TCE-MA-108 | CONTRATAÇÕES DE TI | 2.2 Instrução Normativa SGD/ME nº 94/2022. | 5 | 5 | 4 | 3 |
| TCE-MA-109 | CONTRATAÇÕES DE TI | 2.3 Instrução Normativa SEGES/ME nº 65/2021. | 2 | 2 | 2 | 2 |

### B) Itens com correspondência apenas parcial (sem direta)

| ID | Área | Item | Vínculos parciais | Ocorrências parciais canônicas | Concursos (todas as classes canônicas) | Anos (todas as classes canônicas) |
|---|---|---|---:|---:|---:|---:|
| TCE-MA-010 | ENGENHARIA DE DADOS | 1.5 Ingestão e armazenamento de grande quantidade de dados (big data). | 1 | 1 | 1 | 1 |
| TCE-MA-016 | ENGENHARIA DE DADOS | 6 Modelagem dimensional. | 1 | 1 | 1 | 1 |
| TCE-MA-025 | ENGENHARIA DE SOFTWARE | 1 Conceitos e técnicas do projeto de software. | 3 | 3 | 2 | 2 |
| TCE-MA-038 | ENGENHARIA DE SOFTWARE | 6 Testes de software. | 2 | 0 | 0 | 0 |
| TCE-MA-039 | ENGENHARIA DE SOFTWARE | 6.1 Unitário, integração, funcional, aceitação, desempenho, carga, vulnerabilidade. | 2 | 2 | 2 | 2 |
| TCE-MA-042 | ENGENHARIA DE SOFTWARE | 7 Métricas de software. | 1 | 1 | 1 | 1 |
| TCE-MA-043 | ENGENHARIA DE SOFTWARE | 8. DevOps e integração contínua. | 1 | 0 | 0 | 0 |
| TCE-MA-044 | ENGENHARIA DE SOFTWARE | 8.1 Pipelines de CI/CD. | 1 | 1 | 1 | 1 |
| TCE-MA-045 | ENGENHARIA DE SOFTWARE | 8.2 Build, testes e Deploy automatizados. | 1 | 1 | 1 | 1 |
| TCE-MA-049 | ANÁLISE DE DADOS | 2 Modelagem dimensional aplicada à análise de dados. | 1 | 1 | 1 | 1 |
| TCE-MA-088 | ARQUITETURA DE SOFTWARE | 15 Arquitetura de sistemas web e web standards (W3C). | 1 | 1 | 1 | 1 |
| TCE-MA-093 | GESTÃO E GOVERNANÇA DE TI | 2 Gestão de riscos de TI (ISO 31000, COSO). | 2 | 2 | 2 | 2 |
| TCE-MA-096 | GESTÃO E GOVERNANÇA DE TI | 5 Planejamento estratégico de TI (PETI, PDTI). | 1 | 1 | 2 | 2 |

### Itens somente relacionados

| ID | Área | Item | Ocorrências relacionadas |
|---|---|---|---:|
| TCE-MA-001 | ENGENHARIA DE DADOS | 1 Dado, informação, conhecimento e inteligência. | 1 |
| TCE-MA-029 | ENGENHARIA DE SOFTWARE | 4.1 Requisitos e experiência do usuário. | 1 |
| TCE-MA-033 | ENGENHARIA DE SOFTWARE | 4.5 Projeto centrado no usuário de software. | 1 |
| TCE-MA-100 | GESTÃO E GOVERNANÇA DE TI | 9 Planejamento e gestão estratégicos de TI: PETI, PDTI e Indicadores de desempenho (KPIs, BSC). | 1 |
| TCE-MA-102 | GESTÃO E GOVERNANÇA DE TI | 11 Lei nº 12.527/2011 (Lei de Acesso à Informação). | 1 |

### C) Itens sem correspondência no corpus atual

Para cada item abaixo, não foi encontrada ocorrência nos 56 componentes analisados. Isso não implica impossibilidade de cobrança.

| ID | Área | Item | Folha |
|---|---|---|---|
| TCE-MA-002 | ENGENHARIA DE DADOS | 1.1 Dados estruturados e não estruturados. | sim |
| TCE-MA-003 | ENGENHARIA DE DADOS | 1.2 Dados abertos. | sim |
| TCE-MA-005 | ENGENHARIA DE DADOS | 1 Banco de dados. | não |
| TCE-MA-006 | ENGENHARIA DE DADOS | 1.1 Conceitos básicos. | sim |
| TCE-MA-007 | ENGENHARIA DE DADOS | 1.2 Arquitetura. | sim |
| TCE-MA-008 | ENGENHARIA DE DADOS | 1.3 Estrutura de dados. | sim |
| TCE-MA-011 | ENGENHARIA DE DADOS | 1.6 Banco de dados NoSQL. | sim |
| TCE-MA-013 | ENGENHARIA DE DADOS | 3 Abordagem relacional. | sim |
| TCE-MA-014 | ENGENHARIA DE DADOS | 4 Normalização das estruturas de dados. | sim |
| TCE-MA-017 | ENGENHARIA DE DADOS | 7 Linguagem de consulta estruturada (SQL). | sim |
| TCE-MA-018 | ENGENHARIA DE DADOS | 8 Linguagem de definição de dados (DDL). | sim |
| TCE-MA-019 | ENGENHARIA DE DADOS | 9 Linguagem de manipulação de dados (DML). | sim |
| TCE-MA-021 | ENGENHARIA DE DADOS | 10.1 Noções de administração de dados e de banco de dados. | sim |
| TCE-MA-026 | ENGENHARIA DE SOFTWARE | 2 Processo interativo e incremental. | sim |
| TCE-MA-030 | ENGENHARIA DE SOFTWARE | 4.2 Histórias do usuário. | sim |
| TCE-MA-031 | ENGENHARIA DE SOFTWARE | 4.3 Critérios de aceitação. | sim |
| TCE-MA-032 | ENGENHARIA DE SOFTWARE | 4.4 Prototipação. | sim |
| TCE-MA-034 | ENGENHARIA DE SOFTWARE | 4.6 Storytelling. | sim |
| TCE-MA-036 | ENGENHARIA DE SOFTWARE | 5.1 Minimum viable product (MVP). | sim |
| TCE-MA-040 | ENGENHARIA DE SOFTWARE | 6.2 Ferramentas para automatização de testes. | sim |
| TCE-MA-041 | ENGENHARIA DE SOFTWARE | 6.3 Análise estática de código e cobertura (SonarQube). | sim |
| TCE-MA-047 | ENGENHARIA DE SOFTWARE | 8.4 Monitoramento e observabilidade. | sim |
| TCE-MA-048 | ANÁLISE DE DADOS | 1 Uso de banco de dados relacionais na análise de dados. | sim |
| TCE-MA-051 | ANÁLISE DE DADOS | 3.1 Modelo de referência CRISP‐DM. | sim |
| TCE-MA-056 | ANÁLISE DE DADOS | 3.6 Análise de agrupamentos (clusterização). | sim |
| TCE-MA-057 | ANÁLISE DE DADOS | 3.7 Detecção de anomalias. | sim |
| TCE-MA-059 | ANÁLISE DE DADOS | 3.9 Mineração de texto. | sim |
| TCE-MA-060 | ANÁLISE DE DADOS | 4 Visualização e análise exploratória de dados. | sim |
| TCE-MA-061 | ANÁLISE DE DADOS | 5 Ferramentas de apoio à análise de dados. | não |
| TCE-MA-062 | ANÁLISE DE DADOS | 5.1 Planilhas eletrônicas. | sim |
| TCE-MA-063 | ANÁLISE DE DADOS | 5.2 Linguagem aplicada à análise de dados: Python, R. | sim |
| TCE-MA-064 | ANÁLISE DE DADOS | 5.3 Ferramenta SAS. | sim |
| TCE-MA-071 | INTELIGÊNCIA ARTIFICIAL | 7 Ética, Transparência e Responsabilidade em IA. | sim |
| TCE-MA-072 | INTELIGÊNCIA ARTIFICIAL | 8 Explicabilidade e interpretabilidade de modelos. | sim |
| TCE-MA-073 | INTELIGÊNCIA ARTIFICIAL | 9 Viés algorítmico e discriminação. | sim |
| TCE-MA-074 | ARQUITETURA DE SOFTWARE | 1 Arquitetura de aplicações. | sim |
| TCE-MA-075 | ARQUITETURA DE SOFTWARE | 2 Padrão arquitetural model‐view‐controller (MVC). | sim |
| TCE-MA-077 | ARQUITETURA DE SOFTWARE | 4 Arquitetura orientada a eventos; refatoração e modernização de aplicações. | sim |
| TCE-MA-079 | ARQUITETURA DE SOFTWARE | 6 Padrões de design de software. | sim |
| TCE-MA-080 | ARQUITETURA DE SOFTWARE | 7 Técnicas de componentização de software. | sim |
| TCE-MA-082 | ARQUITETURA DE SOFTWARE | 9 API Gateway. | sim |
| TCE-MA-083 | ARQUITETURA DE SOFTWARE | 10 Noções de servidores de aplicações. | sim |
| TCE-MA-084 | ARQUITETURA DE SOFTWARE | 11 Conteinerização de aplicação. | sim |
| TCE-MA-085 | ARQUITETURA DE SOFTWARE | 12 Serviços de mensageria. | sim |
| TCE-MA-086 | ARQUITETURA DE SOFTWARE | 13 Padrões: SOAP, REST, gRPC, XML, XSLT, UDDI, WSDL, JSON, RMI, XML HTTPRequest. | sim |
| TCE-MA-087 | ARQUITETURA DE SOFTWARE | 14 Gerência de configuração de software (GIT). | sim |
| TCE-MA-089 | ARQUITETURA DE SOFTWARE | 16 Arquitetura de soluções mobile. | sim |
| TCE-MA-090 | ARQUITETURA DE SOFTWARE | 17 Padrões de projeto. | sim |
| TCE-MA-091 | ARQUITETURA DE SOFTWARE | 18 Autenticação única (single sign‐on). | sim |
| TCE-MA-098 | GESTÃO E GOVERNANÇA DE TI | 7 Gestão de processos (BPMN, melhoria contínua). | sim |
| TCE-MA-099 | GESTÃO E GOVERNANÇA DE TI | 8 Compliance e conformidade normativa. | sim |
| TCE-MA-104 | GESTÃO E GOVERNANÇA DE TI | 13 Governança de dados por meio da metodologia do DAMA‐DMBoK (data management body of knowledge). | sim |

## 3.4 — Recorrência temática

Os temas abaixo são agrupamentos analíticos pós-auditoria, não substituem `tema_principal` e aceitam múltiplos rótulos. A tabela separa componentes, concursos e anos para não tratar questões do mesmo certame como observações independentes.

| Agrupamento temático | Componentes | Concursos distintos | Anos distintos |
|---|---:|---:|---:|
| Segurança da informação e cibersegurança | 13 | 11 | 9 |
| Controle externo, auditoria geral e direito público | 10 | 8 | 6 |
| Governança e gestão de serviços de TI | 8 | 7 | 6 |
| Contratações e gestão contratual de TI | 7 | 6 | 5 |
| Engenharia e análise de dados | 6 | 6 | 4 |
| Métodos ágeis e gestão de projetos | 6 | 6 | 5 |
| Engenharia de software e práticas de desenvolvimento | 5 | 4 | 4 |
| Infraestrutura e redes | 5 | 5 | 4 |
| Inteligência artificial e aprendizado de máquina | 5 | 5 | 4 |
| Sustentabilidade e emergência climática | 2 | 2 | 2 |

## 3.5 — Recência descritiva

| Período | Componentes | Concursos distintos | Temas mais presentes no período |
|---|---:|---:|---|
| 2015–2018 | 13 | 5 | Controle externo, auditoria geral e direito público (3); Métodos ágeis e gestão de projetos (3); Segurança da informação e cibersegurança (3); Engenharia de software e práticas de desenvolvimento (2) |
| 2019–2022 | 9 | 4 | Segurança da informação e cibersegurança (3); Engenharia e análise de dados (2); Controle externo, auditoria geral e direito público (1); Contratações e gestão contratual de TI (1) |
| 2023–2026 | 34 | 14 | Segurança da informação e cibersegurança (7); Governança e gestão de serviços de TI (6); Controle externo, auditoria geral e direito público (6); Contratações e gestão contratual de TI (5) |

No período 2015–2018, a amostra combina controle externo, contratações, métodos ágeis/engenharia de software e segurança. Em 2019–2022, o número de componentes é menor e inclui desenvolvimento seguro, segurança organizacional, IA/dados e métodos ágeis. Em 2023–2026, crescem no corpus os registros envolvendo IA/MLOps, dados, cibersegurança, governança e contratações. Essa sequência descreve a composição da amostra e não é usada como inferência de cobrança futura.

## 3.6 — Forma de cobrança

As formas também são multirrótulo; seus percentuais usam os 56 componentes como denominador e, por isso, não somam 100%.

| Forma | Componentes | Percentual |
|---|---:|---:|
| conceitual | 35 | 62,5% |
| situação-problema | 11 | 19,6% |
| estudo de caso | 9 | 16,1% |
| análise técnica | 19 | 33,9% |
| aplicação normativa | 23 | 41,1% |
| projeto/arquitetura | 3 | 5,4% |
| peça técnica | 9 | 16,1% |

### Combinações observadas

| Combinação | Componentes | Percentual |
|---|---:|---:|
| conceitual | 14 | 25,0% |
| conceitual + aplicação normativa | 11 | 19,6% |
| conceitual + análise técnica | 7 | 12,5% |
| estudo de caso + aplicação normativa + peça técnica | 5 | 8,9% |
| situação-problema + análise técnica | 5 | 8,9% |
| situação-problema + aplicação normativa | 2 | 3,6% |
| estudo de caso + análise técnica + aplicação normativa | 2 | 3,6% |
| conceitual + situação-problema | 1 | 1,8% |
| conceitual + peça técnica | 1 | 1,8% |
| análise técnica + projeto/arquitetura | 1 | 1,8% |
| situação-problema + projeto/arquitetura | 1 | 1,8% |
| estudo de caso + análise técnica | 1 | 1,8% |
| conceitual + análise técnica + projeto/arquitetura | 1 | 1,8% |
| situação-problema + aplicação normativa + peça técnica | 1 | 1,8% |
| aplicação normativa + peça técnica | 1 | 1,8% |
| estudo de caso + análise técnica + peça técnica | 1 | 1,8% |
| situação-problema + análise técnica + aplicação normativa | 1 | 1,8% |

### Forma por extensão/tipo

| Grupo | N | Conceitual | Situação-problema | Estudo de caso | Análise técnica | Aplicação normativa | Projeto/arquitetura | Peça técnica |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Questões curtas (até 20 linhas) | 31 | 22 (71,0%) | 8 (25,8%) | 1 (3,2%) | 10 (32,3%) | 11 (35,5%) | 1 (3,2%) | 0 (0,0%) |
| Questões de 30 linhas | 10 | 8 (80,0%) | 2 (20,0%) | 0 (0,0%) | 5 (50,0%) | 2 (20,0%) | 1 (10,0%) | 0 (0,0%) |
| Outras questões não-peça (>30 linhas) | 6 | 4 (66,7%) | 0 (0,0%) | 2 (33,3%) | 3 (50,0%) | 3 (50,0%) | 1 (16,7%) | 0 (0,0%) |
| Peças técnicas | 9 | 1 (11,1%) | 1 (11,1%) | 6 (66,7%) | 1 (11,1%) | 7 (77,8%) | 0 (0,0%) | 9 (100,0%) |

## 3.7 — O que o comando exige

| Característica | Componentes | Percentual |
|---|---:|---:|
| `exige_memorizacao_normativa` | 31 | 55,4% |
| `exige_aplicacao_pratica` | 26 | 46,4% |
| `exige_proposta_solucao` | 15 | 26,8% |
| `exige_comparacao` | 16 | 28,6% |
| `exige_explicacao_conceitual` | 54 | 96,4% |
| `exige_calculo` | 0 | 0,0% |
| `exige_codigo` | 0 | 0,0% |
| `exige_diagrama` | 0 | 0,0% |
| `exige_conhecimento_legislacao` | 14 | 25,0% |

### Questões versus peças técnicas

| Característica | Questões/estudos (n=47) | Peças (n=9) |
|---|---:|---:|
| `exige_memorizacao_normativa` | 23 (48,9%) | 8 (88,9%) |
| `exige_aplicacao_pratica` | 18 (38,3%) | 8 (88,9%) |
| `exige_proposta_solucao` | 7 (14,9%) | 8 (88,9%) |
| `exige_comparacao` | 13 (27,7%) | 3 (33,3%) |
| `exige_explicacao_conceitual` | 45 (95,7%) | 9 (100,0%) |
| `exige_calculo` | 0 (0,0%) | 0 (0,0%) |
| `exige_codigo` | 0 (0,0%) | 0 (0,0%) |
| `exige_diagrama` | 0 (0,0%) | 0 (0,0%) |
| `exige_conhecimento_legislacao` | 8 (17,0%) | 6 (66,7%) |

### Características por categoria do órgão

| Categoria | N | Memorização normativa | Aplicação prática | Proposta | Comparação | Explicação conceitual | Cálculo | Código | Diagrama | Legislação |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 46 | 28 (60,9%) | 23 (50,0%) | 13 (28,3%) | 13 (28,3%) | 44 (95,7%) | 0 (0,0%) | 0 (0,0%) | 0 (0,0%) | 14 (30,4%) |
| B | 6 | 1 (16,7%) | 2 (33,3%) | 1 (16,7%) | 2 (33,3%) | 6 (100,0%) | 0 (0,0%) | 0 (0,0%) | 0 (0,0%) | 0 (0,0%) |
| C | 4 | 2 (50,0%) | 1 (25,0%) | 1 (25,0%) | 1 (25,0%) | 4 (100,0%) | 0 (0,0%) | 0 (0,0%) | 0 (0,0%) | 0 (0,0%) |

## 3.8 — Peças técnicas

| Concurso | Ano | Documento | Tema | Situação | Conhecimentos exigidos | Norma/legislação | Linhas | Pontos | Correspondência |
|---|---:|---|---|---|---|---|---:|---:|---|
| tce_rj_2021_ace_ti | 2021 | parecer | Auditoria de contratações de soluções de TIC | Parecer sobre seis achados de auditoria em contratações de TIC. | avaliar o achado I — riscos e ETP; avaliar o achado II — inexigibilidade e planejamento; avaliar o achado III — duração de serviço contínuo; avaliar o achado IV — DOD e requisitos; avaliar o achado V — equipe e aprovação do ETP; avaliar o achado VI — pregão, julgamento, habilitação e adjudicação | SISP; IN SGD/ME nº 1/2019; Lei nº 8.666/1993; Lei nº 10.520/2002 | 50 | 40,00 | parcial |
| tcdf_2024_ace_ti_infra | 2024 | informação | Modelos de rede OSI e TCP/IP | Informação técnica solicitada após problema na estrutura de rede do TCDF. | estrutura de informação do Manual de Redação Oficial do TCDF; sete camadas do modelo OSI; cinco camadas do modelo TCP/IP | modelo OSI; modelo TCP/IP; Manual de Redação Oficial do TCDF — 2.ª edição | 50 | 40,00 | inexistente |
| tce_ms_2025_ace_ti | 2025 | parecer | Parecer sobre contratação direta e execução de contrato de TI | Contratação direta de sistema com planejamento deficiente, análise técnica insuficiente, pagamento por horas e aditivo de 35%. | inexigibilidade e três pressupostos legais; finalidade e deficiência do ETP e princípio violado; finalidade e deficiência da análise técnica e itens de verificação; pagamento por esforço, riscos, alternativa por resultados e SLA; legalidade do aditivo e limite percentual | Lei n.º 14.133/2021; IN SGD/ME n.º 94/2022; Lei n.º 9.784/1999; ITIL; COBIT; SLA; pontos de função | 60 | 55,00 | direta |
| tce_pr_2024_auditor_informatica | 2024 | parecer | Contratação de equipamentos de TI no SISP | Divergências entre áreas administrativa e de TI na compra de servidores. | composição e instituição da equipe de planejamento; normas e fases da contratação; dispensa e condução da contratação; pesquisa de preços | Lei n.º 14.133/2021; IN SGD/ME n.º 94/2022; SISP | 60 | 20,00 | direta |
| tcdf_2023_ace_sistemas | 2023 | parecer | Adequação institucional à LGPD | Parecer para subsidiar atualização normativa do TCDF quanto à LGPD. | introdução e características da LGPD; controlador e responsabilidades; operador e responsabilidades; encarregado e responsabilidades; quatro recomendações | Lei n.º 13.709/2018; Manual de Redação Oficial do TCDF | 50 | 40,00 | direta |
| tce_sc_2022_auditor_cc | 2022 | relatório técnico | Sistema de gestão da segurança da informação | Relatório técnico sobre programa de vulnerabilidades de universidade com muitos usuários e endpoints. | políticas e organização de segurança da informação; segurança em recursos humanos; controle de acesso | NBR ISO/IEC 27001:2013; NBR ISO/IEC 27002 | 90 | 40,00 | direta |
| tce_pr_2016_analista_informatica | 2016 | parecer | Avaliação de relatório sobre qualidade, agilidade, projetos e métricas | Parecer sobre proposições corretas e incorretas de consultoria de software. | qualidade de software; método ágil; gerenciamento de projetos e estimativas | CMMI-DEV 1.2; MPS.BR 2016; Scrum 2016; PMBOK 5; APF 4.3 | 60 | 20,00 | parcial |
| tcu_2015_aufc_ti | 2015 | parecer | Contratação e gestão de contratos de soluções de TI | Parecer de auditoria sobre sete contratos de TI de órgão do SISP. | conformidade do PDTI; conformidade de sete contratos de soluções de TI | IN SLTI/MPOG n.º 2/2008; IN SLTI/MP n.º 4/2014; SISP | 50 | 40,00 | parcial |
| tcu_2026_aufc_auditoria_ti | 2026 | parecer | Auditoria de contratação de solução SaaS | Três achados em contratação de SaaS para gestão documental. | TCO e formação do preço estimado; pagamento, SLA, reversibilidade e proteção de dados; segregação e qualificação dos fiscais; conclusão e medidas corretivas | Lei n.º 14.133/2021; IN SGD/ME n.º 94/2022; LGPD; SaaS | 50 | 30,00 | direta |

Nas nove peças, **7** usam aplicação normativa, **6** foram classificadas como estudo de caso e **8** exigem proposta ou medida corretiva. Os documentos solicitados foram pareceres (7), informação (1) e relatório técnico (1). O corpus é pequeno e concentrado em órgãos de controle.

## 3.9 — Estrutura dos padrões de resposta do CEBRASPE

Os comandos contêm de **2 a 6 tópicos**, com mediana **3**. Todos os 56 registros possuem padrão oficial e quesitos armazenados. A rubrica segue os tópicos numerados do comando, mas frequentemente os decompõe em níveis de atendimento ou subelementos.

| Característica estrutural | Componentes | Percentual |
|---|---:|---:|
| definição conceitual | 19 | 33,9% |
| justificativa/fundamentação | 16 | 28,6% |
| aplicação ao caso | 26 | 46,4% |
| exemplos | 6 | 10,7% |
| proposição de medidas | 15 | 26,8% |
| avaliação de conformidade | 17 | 30,4% |

A pontuação aparece fragmentada em dois ou mais valores explícitos no comando em **52 componentes (92,9%)**. Nas peças, mesmo quando o comando não explicita cada parcela, os padrões organizam a correção por achados ou blocos. A banca atribui crédito por cobertura graduada dos elementos pedidos, não apenas por uma conclusão global.

## 3.10 — Diferenças entre tipos de órgão

| Categoria | Componentes | Geral | Peças | Legislação | Aplicação prática | Direta | Parcial | Relacionada | Inexistente | Temas mais presentes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| A | 46 | 11 | 9 | 14 | 23 | 17 | 14 | 3 | 12 | Segurança da informação e cibersegurança (11); Controle externo, auditoria geral e direito público (10); Contratações e gestão contratual de TI (7); Governança e gestão de serviços de TI (5) |
| B | 6 | 1 | 0 | 0 | 2 | 2 | 3 | 1 | 0 | Inteligência artificial e aprendizado de máquina (2); Engenharia e análise de dados (2); Governança e gestão de serviços de TI (2); Métodos ágeis e gestão de projetos (1) |
| C | 4 | 1 | 0 | 0 | 1 | 1 | 2 | 0 | 1 | Segurança da informação e cibersegurança (2); Governança e gestão de serviços de TI (1); Engenharia de software e práticas de desenvolvimento (1); Sustentabilidade e emergência climática (1) |

A categoria A concentra 46 dos 56 componentes e todas as nove peças técnicas, além da maior parte das questões gerais de controle externo e das aplicações normativas. A categoria B tem seis componentes, com dados/IA e uma avaliação extensa de práticas ágeis e governança. A categoria C tem quatro componentes, concentrados em governança, criptografia, DevSecOps e uma questão geral. As amostras B e C são pequenas; não há concursos D ou E no corpus atual, portanto não há base para uma comparação descritiva dessas categorias.

## LIMITAÇÕES DO CORPUS

- A amostra não é aleatória e não representa todo o universo de provas do CEBRASPE.
- Foram incluídos somente concursos localizados e documentalmente confirmados nas fases anteriores.
- Há forte concentração em órgãos de controle e fiscalização (categoria A).
- Os editais e perfis dos cargos diferem entre si, mesmo quando classificados na mesma categoria.
- O período 2015–2026 contém mudanças tecnológicas relevantes; uma mesma denominação pode ter conteúdo histórico distinto.
- Houve mudanças legislativas e de versões de normas; correspondência conceitual não implica identidade normativa.
- Existem apenas nove peças técnicas, todas ligadas a órgãos de controle.
- Questões de um mesmo concurso não são observações independentes.
- Ausência de ocorrência não significa ausência de possibilidade de cobrança.
- A correspondência temática e os agrupamentos recorrentes envolvem julgamento analítico, ainda que documentado e auditado.
- As contagens por área e tema são multirrótulo e não podem ser somadas para obter o total do corpus.

## Nota de interpretação

Este relatório apresenta frequências históricas, cobertura do edital atual e diferenças observadas no corpus analisado. Ele não contém ranking preditivo, probabilidade, chance de cobrança ou recomendação de estudo.
