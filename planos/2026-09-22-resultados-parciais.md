# Sessão de 22/09/2026 — correção específica e gerais refeitos

Estado da bateria: parcial. Os 45 itens específicos foram corrigidos objetivamente; os 15 itens gerais substitutos ainda não foram resolvidos. A análise consolidada e os retestes serão fechados depois dos gerais e do recebimento das confianças.

## Resultado objetivo dos conhecimentos específicos

| Bloco | Resultado | Percentual | Tempo |
|---|---:|---:|---:|
| E01 — Engenharia de Dados / Projeto e Modelagem de Dados | 7/10 | 70% | 28:39 |
| E02 — Engenharia de Software / Engenharia de Requisitos | 7/10 | 70% | 24:38 |
| E03 — Análise de Dados / Modelagem Dimensional | 4/10 | 40% | 26:22 |
| E04 — Arquitetura de Software / Microsserviços | 8/10 | 80% | 09:24 |
| E05 — Gestão e Governança de TI / COBIT 2019 | 1/5 | 20% | 12:31 |
| **Total** | **27/45** | **60%** | **1:41:34** |

Não há tópico consolidado. As confianças 1, 2 ou 3 ainda precisam ser informadas para as 18 questões erradas.

## Diagnósticos dos erros específicos

| Bloco | Questão | Marcada → gabarito | Regra correta | Conceito confundido | Mecanismo do distrator |
|---|---|---|---|---|---|
| E01 | #1688661 | D → C | Seleção filtra tuplas, projeção escolhe atributos e junção combina relações; tupla equivale a linha | Seleção/projeção confundidas com junção | Alternativa D preserva apenas a assertiva III e induz a descartar a assertiva I |
| E01 | #95915 | C → E | Entidade forte vira relação com seus atributos simples; N:M exige relação própria e atributo multivalorado exige relação cuja chave inclui a chave da entidade proprietária | Mapeamento de N:M e de atributo multivalorado | Alternativa C aplica indevidamente a regra de 1:N ao relacionamento N:M |
| E01 | #865023 | A → D | Manipulação abrange consultas e alterações; construção grava os registros; definição estabelece estruturas e tipos | Fronteiras entre definição, construção e manipulação do banco | Alternativa A exclui a assertiva III, embora declarar tipos pertença à definição |
| E02 | #553339 | C → D | Requisitos fascinantes podem cativar o usuário; modelos de requisitos podem ser orientados a cenários, classes, comportamento e fluxo; negociação equilibra necessidades, custo e prazo | Categorias de requisitos e atividades da engenharia de requisitos | Alternativa C induz a rejeitar a assertiva I e mantém apenas II e III |
| E02 | #1685957 | E → B | Requisitos funcionais descrevem serviços e comportamentos; requisitos de domínio podem ser funcionais ou não funcionais; não funcionais impõem restrições | Requisito de domínio tratado como exclusivamente funcional | Alternativa E descarta simultaneamente as assertivas verdadeiras I e III |
| E02 | #1545953 | B → C | Elicitação usa stakeholders, conhecimento do domínio, ambiente operacional e ambiente organizacional como fontes | Fontes de elicitação confundidas com uma classificação simplificada de requisitos | Alternativa B reduz toda necessidade a requisito funcional e toda restrição a não funcional |
| E03 | #3082594 | E → B | Tabela fato registra eventos no grão definido, com medidas e chaves para dimensões; dimensão guarda contexto descritivo | Tabela fato confundida com tabela dimensão | A presença de data e outros contextos descritivos atrai para a alternativa E |
| E03 | #3082723 | C → B | No snowflake, atributos descritivos e hierarquias ficam distribuídos em tabelas dimensionais normalizadas | Conteúdo de dimensão confundido com conteúdo da fato | Alternativa C descreve medidas e chaves estrangeiras típicas da tabela fato |
| E03 | #2165890 | A → B | Esquema estrela possui uma tabela fato ligada diretamente a uma tabela por dimensão; constelação compartilha dimensões entre múltiplas fatos | Estrela confundida com constelação de fatos | O termo estrutura composta sugere incorretamente a alternativa A |
| E03 | #621110 | D → A | Os grãos fundamentais de fatos são transação, snapshot periódico e snapshot acumulado; snowflake normaliza dimensões, reduz redundância e aumenta joins | Tipos de tabela fato e efeitos da normalização dimensional | Alternativa D inverte os efeitos do snowflake sobre espaço e navegação |
| E03 | #342776 | C → A | Na abordagem Kimball, a integração empresarial depende de arquitetura dimensional coordenada; marts isolados por área não caracterizam, sozinhos, essa abordagem | Data warehouse dimensional integrado confundido com data mart autônomo | Alternativa C parece correta por mencionar modelagem dimensional, mas omite dimensões conformadas e integração |
| E03 | #1570630 | B → C | Tipo de licitação é dimensão, não fato; organização hierárquica admite snowflake; modelo dimensional aumenta redundância e é voltado à consulta | Fato, dimensão e efeito da desnormalização | A contagem B decorre de aceitar apenas uma entre as assertivas II e III |
| E04 | #3966304 | Errado → Certo | Microsserviços devem idealmente possuir dados sob controle próprio para favorecer implantação independente e baixo acoplamento | Banco compartilhado confundido com padrão de autonomia de dados | A generalização de que sistemas corporativos precisam de base central induz a marcar errado |
| E04 | #2997209 | Errado → Certo | No contexto cobrado, serviços de API operam recursos com GET, POST, PATCH, PUT e DELETE | Conjunto operacional de métodos de API confundido com todos os métodos existentes no HTTP | A palavra “apenas” induz a rejeitar o item pela existência de outros métodos HTTP fora do conjunto cobrado |
| E05 | #3090396 | A → D | COBIT 2019 define seis princípios para o sistema de governança e três para o framework de governança | Princípios do sistema confundidos com princípios do framework | Alternativa A usa a contagem três, correta para o outro conjunto de princípios |
| E05 | #2591855 | A → E | EDM reúne objetivos de governança; APO, BAI, DSS e MEA reúnem objetivos de gestão | Governança confundida com planejamento e gestão | APO parece estratégico, mas continua sendo domínio de gestão |
| E05 | #1856879 | D → B | Capacidade e disponibilidade são práticas do ITIL 4 e correspondem no COBIT ao BAI04 Managed Availability and Capacity | BAI04 confundido com objetivos de planejamento do domínio APO | Alternativa D desloca capacidade e disponibilidade para APO e restringe indevidamente o ITIL |
| E05 | #1857278 | E → A | Risco de negócio gerenciado pertence à dimensão financeira; otimização de custos de processos pertence à dimensão interna do BSC | Metas empresariais do COBIT classificadas na dimensão intuitiva, não na oficial | A palavra “risco” atrai para cliente e “custos” para financeira, invertendo as classificações |

## Conhecimentos gerais — cadernos substitutos

Filtros comuns aplicados: finalidade `conteúdo novo`; banca `CEBRASPE (CESPE)`; modalidade `Múltipla escolha`; universo `Objetivas (todas)`; opção `Remover as que resolvi`; anuladas e desatualizadas removidas; anos `2022, 2023, 2024, 2025 e 2026`. Não houve ampliação de modalidade, banca ou período.

| Bloco | Disciplina e assunto | Questões | Saldo recente validado | Caderno |
|---|---|---:|---:|---|
| G01-R1 | Língua Portuguesa — Interpretação de Textos (Compreensão) | 5 | 328 | [103986520](https://www.tecconcursos.com.br/questoes/cadernos/103986520) |
| G02-R1 | Raciocínio Lógico — Lógica de Proposições | 5 | 124 | [103986536](https://www.tecconcursos.com.br/questoes/cadernos/103986536) |
| G03-R1 | Direito Administrativo — Organização Administrativa | 5 | 113 | [103986554](https://www.tecconcursos.com.br/questoes/cadernos/103986554) |

Os cadernos gerais antigos G01, G02 e G03 de 21/09/2026 foram substituídos por estes e não devem ser resolvidos nesta bateria.

## Microresumos antes da resolução

### G01-R1 — Interpretação de Textos

- Inferência correta precisa ser sustentada pelo texto; plausibilidade externa não basta.
- Reescrita deve preservar relações lógicas, modalidade, intensidade e escopo de negação.
- Pronome ou expressão referencial pode retomar uma ideia inteira, não apenas o substantivo mais próximo.
- Conector aparentemente sinônimo pode alterar causa, consequência, concessão ou conclusão.
- Separe voz do autor, voz citada e informação atribuída a terceiros.

### G02-R1 — Lógica de Proposições

- Sentença aberta, ordem, pergunta e exclamação sem valor lógico não são proposições.
- O “ou” lógico é inclusivo, salvo indicação expressa de exclusividade.
- `p → q` só é falsa com `p` verdadeira e `q` falsa; recíproca e inversa não são equivalentes.
- `p → q` equivale a `¬p ∨ q` e à contrapositiva `¬q → ¬p`.
- Ao negar conectivos, aplique De Morgan e negue cada componente; não preserve o conectivo original.

### G03-R1 — Organização Administrativa

- Desconcentração distribui competências dentro da mesma pessoa; descentralização envolve outra pessoa ou delegatário.
- Autarquia é criada por lei específica; empresa pública, sociedade de economia mista e fundação autorizada dependem de autorização legal e constituição posterior.
- Vinculação da entidade indireta ao ministério supervisor não cria subordinação hierárquica.
- Agência executiva e agência reguladora não são novas espécies universais de pessoa jurídica: a primeira é qualificação; a segunda costuma ser autarquia sob regime especial.
- Personalidade de direito privado não afasta concurso, controle, licitação e demais incidências de direito público previstas no ordenamento.

## Pendências para fechar a primeira bateria

1. Resolver somente os três cadernos gerais substitutos.
2. Informar, para cada questão geral errada ou duvidosa, a confiança 1, 2 ou 3.
3. Informar a confiança dos 18 erros específicos: E01 `7, 9, 10`; E02 `6, 7, 10`; E03 `2, 3, 5, 8, 9, 10`; E04 `1, 5`; E05 `1, 3, 4, 5`.
4. Após esses dados, consolidar o diagnóstico da bateria e agendar os retestes.
