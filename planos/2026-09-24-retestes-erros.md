# D02 — bateria de recuperação orientada pelos erros

Data de criação: 24/09/2026.

Finalidade: reteste e recuperação imediata dos assuntos com maior concentração de erros na primeira bateria. Por decisão do aluno, os níveis de confiança não serão exigidos por enquanto; a prioridade será determinada pelo desempenho objetivo acumulado por assunto.

## Distribuição

| Ordem | Bloco | Assunto | Questões | Modalidade | Caderno |
|---:|---|---|---:|---|---|
| 1 | G01 | Direito Administrativo — Administração Indireta | 10 | Múltipla escolha | [104164538](https://www.tecconcursos.com.br/questoes/cadernos/104164538) |
| 2 | G02 | Raciocínio Lógico — Equivalências Lógicas | 5 | Múltipla escolha | [104164025](https://www.tecconcursos.com.br/questoes/cadernos/104164025) |
| 3 | E01 | Análise de Dados — Modelagem Dimensional | 15 | Certo ou errado | [104164562](https://www.tecconcursos.com.br/questoes/cadernos/104164562) |
| 4 | E02 | Gestão e Governança de TI — COBIT 2019 | 10 | Múltipla escolha | [104164582](https://www.tecconcursos.com.br/questoes/cadernos/104164582) |
| 5 | E03A | Engenharia de Dados — Projeto e Modelagem de Dados | 5 | Múltipla escolha | [104164144](https://www.tecconcursos.com.br/questoes/cadernos/104164144) |
| 6 | E03B | Engenharia de Dados — Projeto e Modelagem de Dados | 5 | Múltipla escolha | [104164177](https://www.tecconcursos.com.br/questoes/cadernos/104164177) |
| 7 | E04 | Engenharia de Software — Engenharia de Requisitos | 5 | Múltipla escolha | [104164200](https://www.tecconcursos.com.br/questoes/cadernos/104164200) |
| 8 | E05 | Arquitetura de Software — Microsserviços | 5 | Certo ou errado | [104164225](https://www.tecconcursos.com.br/questoes/cadernos/104164225) |
|  | **Gerais** |  | **15** |  |  |
|  | **Específicos** |  | **45** |  |  |
|  | **Total** |  | **60** |  |  |

Para manter blocos pedagógicos de 5 questões, executar G01 como questões 1–5 e 6–10; E01 como 1–5, 6–10 e 11–15; E02 como 1–5 e 6–10.

Auditoria concluída após a criação: 60 posições, 60 códigos de questão distintos e nenhuma duplicidade entre os oito cadernos válidos.

## Filtros aplicados

Filtros comuns: finalidade `reteste`; banca `CEBRASPE (CESPE)`; universo `Objetivas (todas)`; opção `Remover as que resolvi`; anos `2022, 2023, 2024, 2025 e 2026`; anuladas e desatualizadas removidas; estado das questões `não resolvidas`.

- G01, G02, E02, E03A, E03B e E04: múltipla escolha; sem ampliação de modalidade, período ou banca.
- E01 e E05: o saldo recente em múltipla escolha foi insuficiente; aplicada a primeira expansão prevista para Cebraspe certo ou errado, mantendo 2022–2026. Não houve ampliação de período nem de banca.

## Microresumos

### G01 — Administração Indireta

- Órgão não tem personalidade jurídica; entidade da administração indireta tem personalidade própria.
- Vinculação permite supervisão e controle finalístico, mas não cria hierarquia com o ministério supervisor.
- Autarquia é criada diretamente por lei; empresa pública, sociedade de economia mista e fundação de direito privado têm criação autorizada e dependem de constituição posterior.
- Pelo princípio da especialidade, a entidade atua nas finalidades que a lei lhe atribuiu; autonomia não significa independência.
- Empresa pública admite qualquer forma societária e capital público; sociedade de economia mista é sociedade anônima e admite capital privado sob controle estatal.

### G02 — Equivalências Lógicas

- `p → q` equivale a `¬p ∨ q` e a `¬q → ¬p`; não equivale à recíproca `q → p`.
- A negação de `p → q` é `p ∧ ¬q`, exatamente o único caso em que a condicional é falsa.
- De Morgan troca o conectivo: `¬(p ∨ q) ≡ ¬p ∧ ¬q` e `¬(p ∧ q) ≡ ¬p ∨ ¬q`.
- Em expressões aninhadas, substitua primeiro a condicional externa por `¬A ∨ B`; preserve cada bloco interno entre parênteses.
- O “ou” é inclusivo salvo indicação expressa; não acrescente exclusividade à proposição.

### E01 — Modelagem Dimensional

- O grão define o significado de uma linha da tabela fato e deve ser fixado antes da escolha das medidas e dimensões.
- Fato registra eventos e medidas no grão definido; dimensão fornece contexto descritivo para filtrar, agrupar e rotular.
- Estrela mantém dimensões desnormalizadas e reduz joins; snowflake normaliza hierarquias, reduz redundância e aumenta joins.
- Os grãos fundamentais de fatos são transação, snapshot periódico e snapshot acumulado.
- Na abordagem Kimball, dimensões conformadas integram processos; múltiplas fatos compartilhando dimensões formam uma constelação.

### E02 — COBIT 2019

- São seis princípios do sistema de governança e três princípios do framework; não troque as contagens.
- EDM contém objetivos de governança; APO, BAI, DSS e MEA contêm objetivos de gestão.
- O sistema possui sete componentes: processos; estruturas; princípios/políticas/procedimentos; informação; cultura/ética/comportamento; pessoas/habilidades/competências; serviços/infraestrutura/aplicações.
- Fatores de desenho adaptam o sistema ao contexto; áreas de foco agrupam temas como segurança, DevOps e pequenas empresas.
- Não classifique metas empresariais no BSC apenas por intuição: use a associação oficial entre objetivo e dimensão.

### E03 — Projeto e Modelagem de Dados

- Seleção filtra linhas; projeção escolhe colunas; junção combina relações.
- Modelo conceitual representa o negócio; lógico estrutura dados sem amarrar-se ao SGBD; físico materializa tabelas, tipos, índices e armazenamento.
- Relacionamento N:M gera relação associativa; a chave normalmente combina as chaves das entidades participantes.
- Atributo multivalorado exige relação própria cuja chave inclui a chave da entidade proprietária.
- Definição estabelece estruturas e tipos; construção carrega os dados; manipulação consulta e altera dados.

### E04 — Engenharia de Requisitos

- Requisito funcional descreve serviço ou comportamento; não funcional impõe qualidade ou restrição; requisito de domínio pode pertencer a qualquer dessas classes.
- Elicitação usa stakeholders, domínio, ambiente operacional e contexto organizacional como fontes.
- Elicitar descobre; analisar/modelar organiza; negociar resolve conflitos; especificar documenta; validar verifica adequação às necessidades.
- História de usuário expressa valor e contexto, mas precisa de critérios de aceitação verificáveis.
- Verificação pergunta se o artefato foi construído corretamente; validação pergunta se representa a necessidade correta.

### E05 — Microsserviços

- Cada serviço deve controlar seus dados para preservar autonomia; banco compartilhado aumenta acoplamento.
- API Gateway centraliza preocupações de entrada, mas não deve concentrar toda a lógica de negócio.
- Cadeias longas de chamadas síncronas aumentam latência e propagação de falhas; eventos favorecem desacoplamento.
- Consistência entre serviços costuma ser eventual; saga coordena transações distribuídas com etapas e compensações.
- O limite do serviço deve refletir uma capacidade de negócio ou bounded context e permitir implantação independente.

## Cadernos preliminares descartados

Não resolver os cadernos `104163982`, `104164000`, `104164048`, `104164070`, `104164099`, `104164108` e `104164130`. Eles foram substituídos porque cadernos separados do mesmo filtro apresentaram questões repetidas. Os cadernos válidos estão exclusivamente na tabela desta página.

## Próximo passo

Resolver na ordem indicada. Ao concluir, basta avisar; os resultados serão extraídos da plataforma, corrigidos e comparados com a primeira bateria sem exigir níveis de confiança.