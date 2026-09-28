# Resultados extraídos em 26/09/2026

Foram extraídos os oito cadernos válidos da D02 e os sete preliminares. A plataforma registra 13 cadernos integralmente respondidos e dois substitutos sem respostas naquele caderno: Administração Indireta `104164538` e Modelagem Dimensional `104164562`. Parte das questões desses substitutos foi respondida em preliminares. Isso não exige repetir os cadernos: todos os registros respondidos foram incorporados ao diagnóstico.

## Resultados por caderno

| Assunto | Caderno | Acertos / respondidas | Situação |
|---|---|---:|---|
| Administração Indireta | 104163982 | 5/5 | preliminar respondido |
| Administração Indireta | 104164000 | 4/5 | preliminar respondido |
| Administração Indireta | 104164538 | 0/0 | substituto sem respostas; 10 posições |
| Equivalências Lógicas | 104164025 | 3/5 | válido respondido |
| Modelagem Dimensional | 104164048 | 3/5 | preliminar respondido |
| Modelagem Dimensional | 104164070 | 3/5 | preliminar respondido |
| Modelagem Dimensional | 104164099 | 4/5 | preliminar respondido |
| Modelagem Dimensional | 104164562 | 0/0 | substituto sem respostas; 15 posições |
| COBIT 2019 | 104164108 | 2/5 | preliminar respondido |
| COBIT 2019 | 104164130 | 3/5 | preliminar respondido |
| COBIT 2019 | 104164582 | 7/10 | válido respondido |
| Projeto e Modelagem de Dados | 104164144 | 5/5 | válido respondido |
| Projeto e Modelagem de Dados | 104164177 | 5/5 | válido respondido |
| Engenharia de Requisitos | 104164200 | 3/5 | válido respondido |
| Microsserviços | 104164225 | 4/5 | válido respondido |

A soma das tentativas registradas é 51/70 (72,9%): gerais 12/15 e específicos 39/55. Esse percentual inclui repetição e não equivale a uma bateria de 70 questões distintas. Não foi comparado diretamente aos 35/60 da D01 nem extrapolado para a nota oficial.

## Auditoria das repetições e prioridades

| Assunto | Tentativas respondidas | Códigos distintos respondidos | Códigos com ao menos um erro | Prioridade imediata |
|---|---:|---:|---:|---|
| Administração Indireta | 10 | 8 | 1 | revisão menor; recuperação observada |
| Equivalências Lógicas | 5 | 5 | 2 | erro recorrente em condicional/negação |
| Modelagem Dimensional | 15 | 10 | 4 | recuperação prioritária |
| COBIT 2019 | 20 | 15 | 8 | maior concentração de erros; um gabarito incompatível |
| Projeto e Modelagem de Dados | 10 | 10 | 0 | reduzir recuperação imediata e agendar validação |
| Engenharia de Requisitos | 5 | 5 | 2 | revisar elicitação e leitura por perspectiva |
| Microsserviços | 5 | 5 | 1 | revisar capacidade de negócio versus operação de API |

São 58 questões distintas em 70 tentativas, com 12 repetições. Há 40 códigos sempre acertados, 16 sempre errados e dois com registros de acerto e erro em cadernos diferentes: `3102193` e `3082807`. Sem horários das tentativas, não se presume qual resposta veio depois nem que a divergência prova recuperação. Não se atribui um único percentual de acerto a essa mistura de respostas. Nenhum tópico é consolidado ou domínio 5/5.

## Divergência de gabarito — #2789898

O Tec indica alternativa C, correspondente ao gabarito oficial da questão 38 de Analista de Suporte da ITAIPU/2024. O item II, porém, inverte os números: COBIT 2019 tem 5 objetivos de governança e 35 de gestão, não o contrário. O item III também não corresponde às quatro dimensões do BSC. Portanto, a questão não será usada para ensinar a contagem invertida nem como erro conceitual confirmado nessa contagem. A resposta B do aluno também inclui o item I, inadequado ao distinguir governança de gestão; revisar essa distinção permanece útil.

O [caderno oficial, questão 38](https://cdn.cebraspe.org.br/concursos/itaipu_23/arquivos/924_ITAIPU_004_01.PDF) e o [gabarito definitivo](https://cdn.cebraspe.org.br/concursos/itaipu_23/arquivos/GAB_DEFINITIVO_924_ITAIPU_004_01.PDF) mantêm a divergência. Não há anulação da questão 38 nesse gabarito; a anulada é a questão 39. A divisão EDM/governança e demais domínios/gestão foi conferida na [ISACA](https://www.isaca.org/resources/news-and-trends/industry-news/2019/employing-cobit-2019-for-enterprise-governance-strategy). Dos oito códigos com erro registrados em COBIT, sete são erros utilizáveis e um fica ressalvado.

## Diagnósticos dos erros

| Questão | Regra correta | Conceito confundido | Mecanismo do distrator |
|---|---|---|---|
| #3478556 | Autarquias são pessoas de direito público; fundações estatais podem ser de direito público ou privado | Natureza jurídica da fundação estatal | C generaliza direito público e patrimônio exclusivamente público como definição necessária de toda fundação instituída pelo Estado |
| #3102193 | Chaves substitutas identificam registros de dimensões sem depender da chave natural do negócio | Chave substituta confundida com chave de negócio ou com atributo exclusivo de fato | O item descreve corretamente seu uso em dimensões, mas foi rejeitado |
| #2603864 | A tabela fato registra eventos relacionados a diversas dimensões e, nesse contexto, contém os dados multidimensionais analisados | Dados multidimensionais confundidos com atributos descritivos das dimensões | A menção a multidimensional induz a excluir a tabela fato |
| #3102191 | Identificação de entidade e colunas descritivas caracterizam dimensão; fato representa eventos no grão definido | Fato confundido com dimensão | O item troca o rótulo dimensão por fato mantendo uma descrição plausível de tabela |
| #1906521 | Dimensões possuem chave primária para identificar seus registros | Chave primária tratada como dispensável na dimensão | A desnormalização dimensional induz a rejeitar a necessidade de identificação do registro |
| #3400131 | Área de foco reúne objetivos relacionados a um tópico de governança | Área de foco confundida com políticas e procedimentos | E usa um componente do sistema no lugar do agrupamento temático pedido |
| #3166232 | BAI significa Construir, Adquirir e Implementar, cobrindo desenvolvimento e integração | Construção e mudança confundidas com operação e suporte | D desloca o desenvolvimento para DSS e usa uma tradução inadequada do domínio |
| #3048566 | A fase 2 da implementação avalia onde a organização está e a capacidade atual | Diagnóstico atual confundido com execução da implantação | E responde como chegar à situação desejada, posterior à avaliação descrita |
| #3082807 | O fator problemas relacionados à TI caracteriza pontos de dor atuais | Problemas atuais confundidos com perfil de risco | A palavra severidade aproxima o enunciado da avaliação de risco, mas o pedido descreve problemas existentes |
| #2789308 | A negação de uma condicional é antecedente verdadeiro e consequente falso | Negação confundida com contrapositiva | C preserva a relação original por contraposição em vez de negá-la |
| #2924772 | `p → (q ∧ r)` equivale a `¬p ∨ (q ∧ r)` | Condicional confundida com inversa | C nega antecedente e consequente sem trocar sua direção, operação que não conserva equivalência |
| #3473439 | Continuidade e disponibilidade dos serviços de negócio são objetivo empresarial, relacionado à continuidade gerenciada | Objetivo empresarial confundido com métrica de processo | A descreve tempo de reparação e recuperação, atraindo pela palavra continuidade |
| #3166373 | Preço muito inferior aos concorrentes exige avaliar sustentabilidade financeira do fornecedor | Viabilidade financeira confundida com capacidade técnica | B é preocupação pertinente em seleção, mas não a mais diretamente indicada pelo preço descrito |
| #1942658 | Selecionar implementações desalinhadas à estratégia caracteriza risco de decisão de investimento em TI | Escolha de investimento confundida com arquitetura corporativa | C atrai pela palavra implementação, mas o erro central é priorização estratégica |
| #3048446 | Etnografia envolve imersão e observação no ambiente de trabalho | Técnica de observação confundida com cenário de uso | D remete ao ambiente operacional, mas não descreve imersão do analista |
| #1914950 | Leitura por perspectiva inspeciona requisitos com roteiro sob pontos de vista de stakeholders | Leitura por perspectiva confundida com leitura por defeitos | E mantém o roteiro correto, mas troca stakeholders por revisores especializados em tipos de erro |
| #2216548 | Microsserviço representa capacidade de negócio com autonomia; não é simples subdivisão das operações de uma API | Limite de serviço confundido com operação de API | O item usa fragmentação e otimização como vantagens genéricas para ocultar a definição incorreta |

O código #2789898 permanece documentado separadamente pela divergência de gabarito. Diagnósticos por código foram deduplicados; o segundo erro em #2603864 reforça a prioridade, sem criar uma nova questão na contagem.

## Retestes agendados

As datas individuais de resolução não foram extraídas. Para evitar atribuir datas fictícias, usa-se a correção de 26/09/2026 como referência desta rodada; os retestes são pendências para as próximas baterias, não cadernos adicionais para resolver hoje.

| Data | Escopo | Quantidade e condição |
|---|---|---|
| 29/09/2026 | Projeto e Modelagem de Dados — primeira validação da D01, cujos resultados foram registrados em 22/09 | 10 inéditas sem releitura, em dois segmentos de 5; ≥80%; preservar a nova evidência 10/10 da D02 |
| 01/10/2026 | Português e conteúdos gerais da primeira correção registrada em 24/09 | blocos de 5; priorizar os erros ainda observados e usar questões não resolvidas |
| 03/10/2026 | COBIT, Modelagem Dimensional, Equivalências, Requisitos, Microsserviços e Administração Indireta — D+7 desta correção | 5 não resolvidas por assunto; sem releitura; integrar à meta 15 gerais/45 específicas, distribuindo assuntos entre dias se necessário |
| 10/10/2026 | Segundo reteste dos assuntos aprovados em 03/10 | 5 por assunto; ajustar pelo desempenho; não conceder domínio 5/5 antes de dois retestes aprovados |

Para a D03, agendar D+7 a partir da data real de conclusão/correção, após o aluno avisar. Confiança permanece dispensada temporariamente conforme decisão registrada em 24/09.
