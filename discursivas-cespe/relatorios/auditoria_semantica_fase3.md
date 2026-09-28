# Auditoria semântica — Fase 3

## Status

Foram auditados **56 de 56 componentes**. As decisões de correção estão **aplicadas**. A auditoria registrou **37 correções de campos analíticos em 18 componentes**.

Nenhum enunciado, padrão de resposta, URL ou identificador documental integra a lista de campos alteráveis desta auditoria. Não houve pesquisa, download ou incorporação de concurso.

## Método e critérios

Cada registro foi lido na ordem: enunciado integral; padrão e quesitos oficiais; classificação temática e forma de cobrança; itens do conteúdo programático. A correspondência foi julgada pelo conceito efetivamente pontuado, não por palavras isoladas. Menções em trechos declarados unicamente motivadores não foram tratadas automaticamente como conteúdo exigido.

Normas históricas foram preservadas. Quando o processo permanece no edital, mas a norma ou versão mudou, a relação foi mantida como parcial e a identidade com o ato atual foi removida. `exige_conhecimento_legislacao` foi reservado a conhecimento jurídico efetivamente necessário; normas técnicas e frameworks permanecem separados em `exige_memorizacao_normativa`.

## Correções registradas

| Componente | Campo | Valor anterior | Valor corrigido | Fundamento resumido |
|---|---|---|---|---|
| `tce_rj_2021_ace_ti_q1` | `exige_comparacao` | não | não | O comando exige identificar a decisão, expor recursos e delimitar o controle judicial; não solicita comparação entre institutos. |
| `tce_rj_2021_ace_ti_q3` | `itens_correspondentes_tce_ma` | ["GESTÃO E GOVERNANÇA DE TI — 10 Cibersegurança e continuidade de negócios (ISO 27001/22301, 27002, NIST)."] | ["GESTÃO E GOVERNANÇA DE TI — 10 Cibersegurança e continuidade de negócios (ISO 27001/22301, 27002, NIST)."] | O conhecimento efetivamente exigido é segurança em BYOD. Arquitetura de soluções mobile e SSO não equivalem, respectivamente, à política BYOD e aos controles de autenticação citados; o texto motivador também não cria um caso concreto a resolver. |
| `tce_rj_2021_ace_ti_q3` | `area_tce_ma` | ["GESTÃO E GOVERNANÇA DE TI"] | ["GESTÃO E GOVERNANÇA DE TI"] | O conhecimento efetivamente exigido é segurança em BYOD. Arquitetura de soluções mobile e SSO não equivalem, respectivamente, à política BYOD e aos controles de autenticação citados; o texto motivador também não cria um caso concreto a resolver. |
| `tce_rj_2021_ace_ti_q3` | `forma_cobranca` | ["conceitual", "análise técnica"] | ["conceitual", "análise técnica"] | O conhecimento efetivamente exigido é segurança em BYOD. Arquitetura de soluções mobile e SSO não equivalem, respectivamente, à política BYOD e aos controles de autenticação citados; o texto motivador também não cria um caso concreto a resolver. |
| `tce_rj_2021_ace_ti_peca` | `itens_correspondentes_tce_ma` | ["GESTÃO E GOVERNANÇA DE TI — 2 Gestão de riscos de TI (ISO 31000, COSO).", "GESTÃO E GOVERNANÇA DE TI — 6 Contratações de TI no setor público.", "CONTRATAÇÕES DE TI — 1 Gestão de contratação de soluções de TI.", "CONTRATAÇÕES DE TI — 2 Legislação aplicável à contratação de bens e serviços de TI e suas alterações."] | ["GESTÃO E GOVERNANÇA DE TI — 2 Gestão de riscos de TI (ISO 31000, COSO).", "GESTÃO E GOVERNANÇA DE TI — 6 Contratações de TI no setor público.", "CONTRATAÇÕES DE TI — 1 Gestão de contratação de soluções de TI.", "CONTRATAÇÕES DE TI — 2 Legislação aplicável à contratação de bens e serviços de TI e suas alterações."] | A peça cobra Lei nº 8.666/1993 e normas históricas do SISP. Há continuidade conceitual com contratações de TI, mas não identidade documental com a Lei nº 14.133/2021 nem com a IN SGD/ME nº 94/2022. |
| `tcdf_2024_ace_ti_infra_peca` | `forma_cobranca` | ["conceitual", "peça técnica"] | ["conceitual", "peça técnica"] | A situação apenas solicita uma informação descritiva sobre as camadas OSI/TCP-IP. Não há solução do problema de rede nem aplicação de norma ao caso; o formato documental deve permanecer identificado como peça técnica. |
| `tcdf_2024_ace_ti_infra_peca` | `exige_memorizacao_normativa` | não | não | A situação apenas solicita uma informação descritiva sobre as camadas OSI/TCP-IP. Não há solução do problema de rede nem aplicação de norma ao caso; o formato documental deve permanecer identificado como peça técnica. |
| `tcdf_2024_ace_ti_infra_peca` | `exige_aplicacao_pratica` | não | não | A situação apenas solicita uma informação descritiva sobre as camadas OSI/TCP-IP. Não há solução do problema de rede nem aplicação de norma ao caso; o formato documental deve permanecer identificado como peça técnica. |
| `tce_ms_2025_ace_ti_q1` | `exige_comparacao` | sim | sim | O comando exige apresentar conjuntamente benefícios e limitações da infraestrutura e integração para IA, estabelecendo contraste analítico entre efeitos positivos e restrições. |
| `tce_rn_2026_ti_cargo12` | `itens_correspondentes_tce_ma` | ["GESTÃO E GOVERNANÇA DE TI — 10 Cibersegurança e continuidade de negócios (ISO 27001/22301, 27002, NIST)."] | ["GESTÃO E GOVERNANÇA DE TI — 10 Cibersegurança e continuidade de negócios (ISO 27001/22301, 27002, NIST)."] | Tokens, certificados, biometria e MFA são métodos de autenticação; SSO é mecanismo distinto e não foi exigido. A correspondência parcial subsiste pelo item amplo de cibersegurança. |
| `tce_rn_2026_ti_cargo12` | `area_tce_ma` | ["GESTÃO E GOVERNANÇA DE TI"] | ["GESTÃO E GOVERNANÇA DE TI"] | Tokens, certificados, biometria e MFA são métodos de autenticação; SSO é mecanismo distinto e não foi exigido. A correspondência parcial subsiste pelo item amplo de cibersegurança. |
| `tce_rs_2025_auditor_ti_p3` | `forma_cobranca` | ["conceitual", "aplicação normativa"] | ["conceitual", "aplicação normativa"] | Competências do TCE/RS e a distinção entre parecer prévio e julgamento decorrem da Constituição e da legislação orgânica; a resposta depende de conteúdo jurídico normativo. |
| `tce_rs_2025_auditor_ti_p3` | `exige_memorizacao_normativa` | sim | sim | Competências do TCE/RS e a distinção entre parecer prévio e julgamento decorrem da Constituição e da legislação orgânica; a resposta depende de conteúdo jurídico normativo. |
| `tce_rs_2025_auditor_ti_p3` | `exige_conhecimento_legislacao` | sim | sim | Competências do TCE/RS e a distinção entre parecer prévio e julgamento decorrem da Constituição e da legislação orgânica; a resposta depende de conteúdo jurídico normativo. |
| `tce_rs_2025_auditor_ti_p4` | `itens_correspondentes_tce_ma` | ["GESTÃO E GOVERNANÇA DE TI — 10 Cibersegurança e continuidade de negócios (ISO 27001/22301, 27002, NIST)."] | ["GESTÃO E GOVERNANÇA DE TI — 10 Cibersegurança e continuidade de negócios (ISO 27001/22301, 27002, NIST)."] | A menção à LGPD está no texto declarado unicamente motivador. O comando e a rubrica cobram propriedades de segurança e sua correlação com controles técnicos, sem dispositivo legal, comparação ou edição normativa. |
| `tce_rs_2025_auditor_ti_p4` | `forma_cobranca` | ["conceitual"] | ["conceitual"] | A menção à LGPD está no texto declarado unicamente motivador. O comando e a rubrica cobram propriedades de segurança e sua correlação com controles técnicos, sem dispositivo legal, comparação ou edição normativa. |
| `tce_rs_2025_auditor_ti_p4` | `exige_memorizacao_normativa` | não | não | A menção à LGPD está no texto declarado unicamente motivador. O comando e a rubrica cobram propriedades de segurança e sua correlação com controles técnicos, sem dispositivo legal, comparação ou edição normativa. |
| `tce_rs_2025_auditor_ti_p4` | `exige_comparacao` | não | não | A menção à LGPD está no texto declarado unicamente motivador. O comando e a rubrica cobram propriedades de segurança e sua correlação com controles técnicos, sem dispositivo legal, comparação ou edição normativa. |
| `tce_rs_2025_auditor_ti_p4` | `exige_conhecimento_legislacao` | não | não | A menção à LGPD está no texto declarado unicamente motivador. O comando e a rubrica cobram propriedades de segurança e sua correlação com controles técnicos, sem dispositivo legal, comparação ou edição normativa. |
| `tce_rs_2025_auditor_ti_p4` | `ano_norma_cobrada` | [] | [] | A menção à LGPD está no texto declarado unicamente motivador. O comando e a rubrica cobram propriedades de segurança e sua correlação com controles técnicos, sem dispositivo legal, comparação ou edição normativa. |
| `tcdf_2023_ace_sistemas_q2` | `forma_cobranca` | ["conceitual"] | ["conceitual"] | O cenário apenas motiva uma exposição das práticas de XP, Kanban e Scrum. Os fatos não precisam ser usados para resolver um caso e o comando não contrapõe as metodologias, mas exige recordar elementos definidos dos frameworks. |
| `tcdf_2023_ace_sistemas_q2` | `exige_memorizacao_normativa` | sim | sim | O cenário apenas motiva uma exposição das práticas de XP, Kanban e Scrum. Os fatos não precisam ser usados para resolver um caso e o comando não contrapõe as metodologias, mas exige recordar elementos definidos dos frameworks. |
| `tcdf_2023_ace_sistemas_q2` | `exige_aplicacao_pratica` | não | não | O cenário apenas motiva uma exposição das práticas de XP, Kanban e Scrum. Os fatos não precisam ser usados para resolver um caso e o comando não contrapõe as metodologias, mas exige recordar elementos definidos dos frameworks. |
| `tcdf_2023_ace_sistemas_q2` | `exige_comparacao` | não | não | O cenário apenas motiva uma exposição das práticas de XP, Kanban e Scrum. Os fatos não precisam ser usados para resolver um caso e o comando não contrapõe as metodologias, mas exige recordar elementos definidos dos frameworks. |
| `tce_ro_2019_ace_ti_q1` | `itens_correspondentes_tce_ma` | ["ENGENHARIA DE SOFTWARE — 1 Conceitos e técnicas do projeto de software.", "GESTÃO E GOVERNANÇA DE TI — 10 Cibersegurança e continuidade de negócios (ISO 27001/22301, 27002, NIST)."] | ["ENGENHARIA DE SOFTWARE — 1 Conceitos e técnicas do projeto de software.", "GESTÃO E GOVERNANÇA DE TI — 10 Cibersegurança e continuidade de negócios (ISO 27001/22301, 27002, NIST)."] | MVP aparece somente no fragmento motivador. A resposta é uma exposição dos controles da ISO/IEC 27002:2013, sem aplicação a fatos específicos; a referência ao projeto de software e à cibersegurança permanece parcial em razão da edição histórica da norma. |
| `tce_ro_2019_ace_ti_q1` | `forma_cobranca` | ["conceitual", "aplicação normativa"] | ["conceitual", "aplicação normativa"] | MVP aparece somente no fragmento motivador. A resposta é uma exposição dos controles da ISO/IEC 27002:2013, sem aplicação a fatos específicos; a referência ao projeto de software e à cibersegurança permanece parcial em razão da edição histórica da norma. |
| `tce_ro_2019_ace_ti_q1` | `exige_aplicacao_pratica` | não | não | MVP aparece somente no fragmento motivador. A resposta é uma exposição dos controles da ISO/IEC 27002:2013, sem aplicação a fatos específicos; a referência ao projeto de software e à cibersegurança permanece parcial em razão da edição histórica da norma. |
| `tce_mg_2018_ace_cc_q2` | `correspondencia_com_edital_tce_ma` | parcial | parcial | Scrum e práticas ágeis estão no edital atual, mas a questão também exige planning poker e todo o modelo GROW, conteúdos relevantes não explicitados; a correspondência é parcial. |
| `cgm_joao_pessoa_2018_auditor_sistemas_q1` | `exige_conhecimento_legislacao` | não | não | Embora o texto contextual mencione validade jurídica da ICP-Brasil, o comando e a rubrica cobram consequências técnicas de certificados, MD5 e DNS e uma solução operacional, sem conhecimento de dispositivo legal. |
| `tce_pr_2016_analista_informatica_q1` | `correspondencia_com_edital_tce_ma` | parcial | parcial | A questão cobra parte expressamente relacionada a projeto e requisitos, mas acrescenta análise econômica, artefatos e diagramas não individualizados no edital; o software hipotético apenas ilustra a exposição, sem fatos que condicionem a resposta. |
| `tce_pr_2016_analista_informatica_q1` | `forma_cobranca` | ["conceitual"] | ["conceitual"] | A questão cobra parte expressamente relacionada a projeto e requisitos, mas acrescenta análise econômica, artefatos e diagramas não individualizados no edital; o software hipotético apenas ilustra a exposição, sem fatos que condicionem a resposta. |
| `tce_pr_2016_analista_informatica_q1` | `exige_aplicacao_pratica` | não | não | A questão cobra parte expressamente relacionada a projeto e requisitos, mas acrescenta análise econômica, artefatos e diagramas não individualizados no edital; o software hipotético apenas ilustra a exposição, sem fatos que condicionem a resposta. |
| `tce_pr_2016_analista_informatica_peca` | `exige_proposta_solucao` | sim | sim | O parecer não apenas avalia: o comando exige complementar lacunas e a rubrica demanda sugerir proposição adequada quando a proposição auditada estiver errada. |
| `tcu_2015_aufc_ti_p3_q1` | `exige_comparacao` | sim | sim | O núcleo do comando é equilibrar confidencialidade e transparência e tratar os limites entre esses deveres, o que exige contraposição explícita. |
| `sefaz_ce_2021_auditor_ti_q2` | `exige_comparacao` | não | não | Solicitar a descrição de dois tipos de redes neurais não equivale a exigir que sejam comparados; a rubrica pontua citação e descrição separadas. |
| `sefaz_ce_2021_auditor_ti_estudo` | `exige_proposta_solucao` | sim | sim | Para os achados rejeitados, o comando exige sugerir proposições de melhoria apropriadas e a rubrica pontua expressamente essa proposta. |
| `trt10_2025_analista_ti_q1` | `exige_aplicacao_pratica` | não | não | O texto motivador não configura caso concreto. O comando pede pressupostos, objetivos e benefícios de DevSecOps/OWASP SAMM, sem aplicar os conceitos a uma organização específica. |

## Cobertura integral da auditoria

A tabela abaixo explicita os 56 componentes confrontados. “Mantida” significa que todos os 18 campos auditados permaneceram semanticamente adequados; “corrigida” indica ao menos uma mudança documentada acima.

| # | Componente | Concurso | Ano | Tipo | Resultado | Estado no CSV | Correspondência final | Tema final |
|---:|---|---|---:|---|---|---|---|---|
| 1 | `tce_rj_2021_ace_ti_q1` | `tce_rj_2021_ace_ti` | 2021 | questão dissertativa | corrigida | final | inexistente | Controle externo e recursos contra decisão de tribunal de contas |
| 2 | `tce_rj_2021_ace_ti_q2` | `tce_rj_2021_ace_ti` | 2021 | questão dissertativa | mantida | final | direta | Mineração de dados — regras de associação |
| 3 | `tce_rj_2021_ace_ti_q3` | `tce_rj_2021_ace_ti` | 2021 | questão dissertativa | corrigida | final | parcial | Segurança da informação em BYOD |
| 4 | `tce_rj_2021_ace_ti_peca` | `tce_rj_2021_ace_ti` | 2021 | peça de natureza técnica — parecer | corrigida | final | parcial | Auditoria de contratações de soluções de TIC |
| 5 | `tcdf_2024_ace_ti_infra_q1` | `tcdf_2024_ace_ti_infra` | 2024 | questão dissertativa | mantida | final | direta | Gestão de incidentes e de problemas (ITIL v4) |
| 6 | `tcdf_2024_ace_ti_infra_q2` | `tcdf_2024_ace_ti_infra` | 2024 | questão dissertativa | mantida | final | direta | Planejamento da contratação de serviço de TI |
| 7 | `tcdf_2024_ace_ti_infra_peca` | `tcdf_2024_ace_ti_infra` | 2024 | peça de natureza técnica — informação | corrigida | final | inexistente | Modelos de rede OSI e TCP/IP |
| 8 | `tce_ms_2025_ace_ti_q1` | `tce_ms_2025_ace_ti` | 2025 | questão dissertativa | corrigida | final | direta | Inteligência artificial na administração pública |
| 9 | `tce_ms_2025_ace_ti_q2` | `tce_ms_2025_ace_ti` | 2025 | questão dissertativa | mantida | final | direta | Contratação e fiscalização de bens e serviços de TI |
| 10 | `tce_ms_2025_ace_ti_q3` | `tce_ms_2025_ace_ti` | 2025 | questão dissertativa | mantida | final | direta | Gestão de serviços de TI (ITIL v4) |
| 11 | `tce_ms_2025_ace_ti_peca` | `tce_ms_2025_ace_ti` | 2025 | peça de natureza técnica — parecer | mantida | final | direta | Parecer sobre contratação direta e execução de contrato de TI |
| 12 | `tce_rn_2026_ti_cargo4` | `tce_rn_2026_ti` | 2026 | questão dissertativa | mantida | final | direta | Modelagem de dados conceitual, lógica e física |
| 13 | `tce_rn_2026_ti_cargo5` | `tce_rn_2026_ti` | 2026 | questão dissertativa | mantida | final | parcial | Infraestrutura, segurança e continuidade de aplicação web |
| 14 | `tce_rn_2026_ti_cargo12` | `tce_rn_2026_ti` | 2026 | estudo de caso | corrigida | final | parcial | Métodos de autenticação e controle de acesso |
| 15 | `tce_mg_2026_ace_cc_q1` | `tce_mg_2026_ace_cc` | 2026 | questão dissertativa | mantida | final | inexistente | Controle da administração pública em Minas Gerais |
| 16 | `tce_mg_2026_ace_cc_q2` | `tce_mg_2026_ace_cc` | 2026 | questão dissertativa | mantida | final | direta | Técnicas de integração e ingestão de dados |
| 17 | `tce_rs_2025_auditor_ti_p3` | `tce_rs_2025_auditor_ti` | 2025 | questão dissertativa | corrigida | final | inexistente | Competências do TCE/RS no controle externo |
| 18 | `tce_rs_2025_auditor_ti_p4` | `tce_rs_2025_auditor_ti` | 2025 | questão dissertativa | corrigida | final | direta | Propriedades e controles de segurança da informação |
| 19 | `tce_pr_2024_auditor_informatica_q1` | `tce_pr_2024_auditor_informatica` | 2024 | questão dissertativa | mantida | final | inexistente | Endereçamento IPv4 e IPv6 |
| 20 | `tce_pr_2024_auditor_informatica_q2` | `tce_pr_2024_auditor_informatica` | 2024 | questão dissertativa | mantida | final | apenas relacionada | Processamento de dados em lote e em tempo real |
| 21 | `tce_pr_2024_auditor_informatica_q3` | `tce_pr_2024_auditor_informatica` | 2024 | questão dissertativa | mantida | final | inexistente | Julgamento de contas do chefe do Poder Legislativo |
| 22 | `tce_pr_2024_auditor_informatica_q4` | `tce_pr_2024_auditor_informatica` | 2024 | questão dissertativa | mantida | final | inexistente | Risco de auditoria |
| 23 | `tce_pr_2024_auditor_informatica_peca` | `tce_pr_2024_auditor_informatica` | 2024 | peça técnica — parecer | mantida | final | direta | Contratação de equipamentos de TI no SISP |
| 24 | `tce_ac_2024_analista_ti_q1` | `tce_ac_2024_analista_ti` | 2024 | questão dissertativa | mantida | final | direta | Inteligência artificial no controle institucional e social |
| 25 | `tcdf_2023_ace_sistemas_q1` | `tcdf_2023_ace_sistemas` | 2023 | questão dissertativa | mantida | final | parcial | Governança, serviços e segurança de TI |
| 26 | `tcdf_2023_ace_sistemas_q2` | `tcdf_2023_ace_sistemas` | 2023 | questão dissertativa | corrigida | final | direta | Metodologias ágeis de desenvolvimento |
| 27 | `tcdf_2023_ace_sistemas_peca` | `tcdf_2023_ace_sistemas` | 2023 | peça de natureza técnica — parecer | mantida | final | direta | Adequação institucional à LGPD |
| 28 | `tce_sc_2022_auditor_cc_relatorio` | `tce_sc_2022_auditor_cc` | 2022 | peça técnica — relatório técnico | mantida | final | direta | Sistema de gestão da segurança da informação |
| 29 | `tce_ro_2019_ace_ti_q1` | `tce_ro_2019_ace_ti` | 2019 | questão dissertativa | corrigida | final | parcial | Desenvolvimento seguro de sistemas |
| 30 | `tce_mg_2018_ace_cc_q1` | `tce_mg_2018_ace_cc` | 2018 | questão dissertativa | mantida | final | inexistente | Controle externo exercido pelos tribunais de contas |
| 31 | `tce_mg_2018_ace_cc_q2` | `tce_mg_2018_ace_cc` | 2018 | questão dissertativa | corrigida | final | parcial | Scrum e práticas de equipes ágeis |
| 32 | `cgm_joao_pessoa_2018_auditor_sistemas_q1` | `cgm_joao_pessoa_2018_auditor_sistemas` | 2018 | questão dissertativa | corrigida | final | apenas relacionada | Certificados digitais e ICP-Brasil |
| 33 | `tce_pr_2016_analista_informatica_q1` | `tce_pr_2016_analista_informatica` | 2016 | questão dissertativa | corrigida | final | parcial | Fases e artefatos de engenharia de software |
| 34 | `tce_pr_2016_analista_informatica_q2` | `tce_pr_2016_analista_informatica` | 2016 | questão dissertativa | mantida | final | parcial | Processos de engenharia de software |
| 35 | `tce_pr_2016_analista_informatica_q3` | `tce_pr_2016_analista_informatica` | 2016 | questão dissertativa | mantida | final | inexistente | Controle de congestionamento TCP |
| 36 | `tce_pr_2016_analista_informatica_q4` | `tce_pr_2016_analista_informatica` | 2016 | questão dissertativa | mantida | final | parcial | Níveis de capacidade do COBIT 5 |
| 37 | `tce_pr_2016_analista_informatica_peca` | `tce_pr_2016_analista_informatica` | 2016 | peça técnica — parecer | corrigida | final | parcial | Avaliação de relatório sobre qualidade, agilidade, projetos e métricas |
| 38 | `tce_pa_2016_auditor_informatica_q1` | `tce_pa_2016_auditor_informatica` | 2016 | questão dissertativa | mantida | final | inexistente | Desenvolvimento sustentável e gestão municipal |
| 39 | `tcu_2015_aufc_ti_p3_q1` | `tcu_2015_aufc_ti` | 2015 | questão dissertativa | corrigida | final | apenas relacionada | Confidencialidade e transparência na documentação de auditoria |
| 40 | `tcu_2015_aufc_ti_p3_q2` | `tcu_2015_aufc_ti` | 2015 | questão dissertativa | mantida | final | inexistente | Independência das entidades fiscalizadoras superiores |
| 41 | `tcu_2015_aufc_ti_p4_q1` | `tcu_2015_aufc_ti` | 2015 | questão dissertativa | mantida | final | parcial | Identificação de riscos de segurança da informação |
| 42 | `tcu_2015_aufc_ti_p4_peca` | `tcu_2015_aufc_ti` | 2015 | peça de natureza técnica — parecer | mantida | final | parcial | Contratação e gestão de contratos de soluções de TI |
| 43 | `tcu_2026_aufc_auditoria_ti_q1` | `tcu_2026_aufc_auditoria_ti` | 2026 | questão dissertativa | mantida | final | inexistente | Responsabilidade civil do Estado e competências do TCU |
| 44 | `tcu_2026_aufc_auditoria_ti_q2` | `tcu_2026_aufc_auditoria_ti` | 2026 | questão dissertativa | mantida | final | direta | Segurança de pipeline MLOps em nuvem |
| 45 | `tcu_2026_aufc_auditoria_ti_q3` | `tcu_2026_aufc_auditoria_ti` | 2026 | questão dissertativa | mantida | final | parcial | Scrum, TDD e DDD em auditoria de software |
| 46 | `tcu_2026_aufc_auditoria_ti_peca` | `tcu_2026_aufc_auditoria_ti` | 2026 | peça de natureza técnica — parecer | mantida | final | direta | Auditoria de contratação de solução SaaS |
| 47 | `sefaz_se_2025_auditor_ti_q1` | `sefaz_se_2025_auditor_ti` | 2025 | questão dissertativa | mantida | final | direta | Modelagem preditiva |
| 48 | `sefaz_se_2025_auditor_ti_q2` | `sefaz_se_2025_auditor_ti` | 2025 | questão dissertativa | mantida | final | parcial | OLAP e ETL |
| 49 | `sefa_pr_2026_agente_ti_q1` | `sefa_pr_2026_agente_ti` | 2026 | questão dissertativa | mantida | final | apenas relacionada | Planejamento e transformação digital no setor público |
| 50 | `sefaz_ce_2021_auditor_ti_q1` | `sefaz_ce_2021_auditor_ti` | 2021 | questão dissertativa | mantida | final | parcial | Apache Hadoop e processamento distribuído |
| 51 | `sefaz_ce_2021_auditor_ti_q2` | `sefaz_ce_2021_auditor_ti` | 2021 | questão dissertativa | corrigida | final | direta | Deep learning e processamento de linguagem natural |
| 52 | `sefaz_ce_2021_auditor_ti_estudo` | `sefaz_ce_2021_auditor_ti` | 2021 | estudo de caso | corrigida | final | parcial | Avaliação de maturidade ágil e governança de TI |
| 53 | `stj_2024_analista_ti_cargo3` | `stj_2024_analista_ti` | 2024 | questão dissertativa | mantida | final | direta | Implementação do COBIT 2019 |
| 54 | `stj_2024_analista_ti_cargo18` | `stj_2024_analista_ti` | 2024 | questão dissertativa | mantida | final | parcial | Criptografia, certificados digitais e hash |
| 55 | `trt10_2025_analista_ti_q1` | `trt10_2025_analista_ti` | 2025 | questão dissertativa | corrigida | final | parcial | DevSecOps e OWASP SAMM |
| 56 | `trf6_2025_analistas_ti_q1` | `trf6_2025_analistas_ti` | 2025 | questão dissertativa | mantida | final | inexistente | Emergência climática e sustentabilidade |

## Problemas semânticos encontrados

- associação de mecanismos apenas próximos, como SSO e MFA, sem equivalência conceitual;
- uso de itens específicos da legislação atual para questões regidas por normas históricas;
- transformação de textos apenas motivadores em situação-problema ou em exigência legal;
- marcação de comparação quando o comando somente solicitava descrições independentes;
- ausência de marcação de proposta quando a rubrica pontuava uma solução corretiva;
- superestimação de aplicação prática em questões puramente expositivas.

## Rastreabilidade

A justificativa completa, os valores anterior e final de todos os campos, e as referências documentais de cada um dos 56 componentes estão em `dados/fase3_auditoria.json`.
