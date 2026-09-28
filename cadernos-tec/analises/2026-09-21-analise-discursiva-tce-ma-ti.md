# Análise separada — prova discursiva do TCE-MA, Analista de TI

Data da análise: 21/09/2026  
Fonte de delimitação: edital do TCE-MA, Cargo 10, em `documentos de apoio/tce-edital.pdf`.

## Estrutura oficial da prova

A prova discursiva vale 40 pontos e será realizada no turno da tarde, em até quatro horas. Ela contém:

- uma peça de natureza técnica, de até 60 linhas, valendo 20 pontos;
- duas questões discursivas sobre situação-problema da especialidade, de até 30 linhas cada, valendo 10 pontos cada.

O edital prevê avaliação do domínio técnico e do uso da língua portuguesa. Texto fora do espaço próprio ou além do limite de linhas é desconsiderado. Fuga ao tema ou ausência de texto leva a nota zero. O candidato é eliminado se obtiver menos de 20 pontos no conjunto da discursiva.

As fórmulas do edital penalizam erros de português em relação ao total de linhas efetivamente escritas:

- questões: `NQi = NCi − 2 × NEi / TLi`;
- peça: `NP = NC − 4 × NE / TL`;
- nota total: `NPD = NP + NQ1 + NQ2`.

Isso exige respostas completas, bem estruturadas e tecnicamente densas. Aumentar o texto com conteúdo irrelevante continua sendo uma estratégia ruim, pois consome linhas e aumenta a exposição a erros.

## Corpus comparável

Foram localizados e classificados dez itens técnicos discursivos oficiais do Cebraspe em concursos de Tribunais de Contas: TCE-RJ, TCDF, TCE-PR, TCE-MS e TCE-RN. Itens gerais de controle externo foram separados do recorte de TI.

| Tema predominante | Itens | Participação na amostra de 10 |
|---|---:|---:|
| Contratações e auditoria de contratações de TI | 4 | 40% |
| Segurança, identidade e controle de acesso | 2 | 20% |
| ITIL e gestão de serviços | 1 | 10% |
| Mineração e análise de dados | 1 | 10% |
| IA integrada a dados, nuvem, APIs e microsserviços | 1 | 10% |
| Redes e modelos OSI/TCP-IP | 1 | 10% |

A amostra é pequena e serve como sinal direcional. O item de redes veio de uma especialidade de infraestrutura do TCDF e não justifica inserir redes no conteúdo específico do TCE-MA. Redes básicas permanecem apenas no bloco geral de competências digitais, conforme o edital local.

### Itens classificados

| Concurso | Tipo de item | Tema central |
|---|---|---|
| TCE-RJ 2021 | questão | mineração de dados, Apriori, suporte, confiança e lift |
| TCE-RJ 2021 | questão | BYOD, VPN, MFA e política de segurança |
| TCE-RJ 2021 | peça técnica | auditoria de planejamento e execução de contratação de TI |
| TCDF 2024 | questão | incidente e problema no ITIL 4 |
| TCDF 2024 | questão | equipe de planejamento, fases e DFD na IN nº 94/2022 |
| TCDF 2024 | peça técnica | modelos OSI e TCP/IP em uma informação técnica |
| TCE-PR 2024 | peça técnica | contratação de TI, Lei nº 14.133/2021, IN nº 94/2022 e pesquisa de preços |
| TCE-MS 2025 | questão | IA no setor público integrada a nuvem, data lakes, APIs e microsserviços |
| TCE-MS 2025 | peça técnica | achados de auditoria em contratação sob a Lei nº 14.133/2021 |
| TCE-RN 2026 | estudo de caso | autenticação, MFA, IAM, RBAC/ABAC e ISO/IEC 27001/27002 |

## Achado mais forte: peça técnica de contratações

Entre as quatro peças técnicas comparáveis localizadas, três trataram de contratação ou auditoria de contratação de TI:

- TCE-RJ: achados sobre planejamento, estudo técnico preliminar, riscos e ordem de serviço em contratação de TI;
- TCE-PR: parecer envolvendo IN SGD/ME nº 94/2022, Lei nº 14.133/2021, equipe de planejamento, fases da contratação, forma de contratação e pesquisa de preços;
- TCE-MS: análise de achados de auditoria sobre inexigibilidade, ETP, parecer técnico, alterações contratuais e Lei nº 14.133/2021.

Isso torna **Contratações de TI** o primeiro eixo de preparação da peça. O treino deve exigir aplicação da norma aos fatos, identificação da irregularidade, fundamento e recomendação. Apenas reproduzir conceitos não atende ao padrão observado.

## Prioridades temáticas da discursiva

### 1. Contratações de TI — prioridade muito alta

Dominar o encadeamento `necessidade → DFD → equipe de planejamento → ETP → riscos → TR/projeto básico → seleção → gestão e fiscalização`. Treinar Lei nº 14.133/2021, IN SGD/ME nº 94/2022 e IN SEGES/ME nº 65/2021 de forma integrada e aplicada a achados.

### 2. Governança, segurança e serviços — prioridade alta

Treinar resposta situacional sobre incidentes e problemas no ITIL 4; controles, riscos e responsabilidades; autenticação; MFA; IAM; RBAC e ABAC; certificados; ISO/IEC 27001 e 27002; NIST; continuidade e proteção de dados.

### 3. IA, dados e arquitetura aplicados ao setor público — prioridade alta e crescente

O TCE-MS já exigiu benefícios, limites e usos de IA na administração pública em conjunto com nuvem, data lakes, APIs e microsserviços. O treino deve conectar tecnologia a auditoria, detecção de fraude, automação, atendimento, governança, explicabilidade, viés, privacidade e segurança.

### 4. Engenharia e análise de dados — prioridade alta

Treinar problemas de associação, suporte, confiança e lift; classificação, clusterização e detecção de anomalias; qualidade e integração de dados; modelagem, ETL/ELT e uso analítico no controle externo.

### 5. Engenharia e arquitetura de software — prioridade média-alta

Embora a incidência discursiva histórica direta seja menor, o edital atual é amplo. Treinar decisões justificadas sobre requisitos, testes, CI/CD, DevSecOps, microsserviços, eventos, APIs, conteinerização, observabilidade e modernização de legado.

## Formatos que devem ser treinados

O edital do TCE-MA informa “peça de natureza técnica”, sem fixar no programa um único gênero. O ciclo deve alternar:

1. **Parecer técnico:** relatório sintético do caso, fundamentação, análise individual dos pontos e conclusão/recomendação.
2. **Informação ou nota técnica:** identificação do assunto, contexto, análise objetiva, conclusão e encaminhamento.
3. **Relatório de achados:** condição encontrada, critério violado, causa ou risco, efeito e recomendação.

Nas questões de 30 linhas, a estrutura recomendada é: tese inicial curta, um parágrafo por aspecto solicitado e fechamento aplicado ao caso. A resposta deve espelhar todos os comandos do enunciado; as grades do Cebraspe normalmente atribuem pontuação separada a cada aspecto.

## Ciclo semanal de treinamento

| Atividade | Frequência | Distribuição inicial |
|---|---:|---|
| Questão discursiva de até 30 linhas | 2 por semana | uma de governança/segurança/serviços; uma de dados/IA/arquitetura/engenharia |
| Peça técnica de até 60 linhas | 1 por semana | 50% das peças sobre contratações; 50% alternando segurança, governança de dados, IA e arquitetura |
| Simulado completo | a cada 2 semanas | uma peça + duas questões, com limite total de 4 horas |

O treino deve começar com consulta e checklist técnico. Depois de duas semanas, uma das três produções semanais deve ser sem consulta. A correção deve registrar separadamente:

- pontos técnicos pedidos e efetivamente atendidos;
- fundamento normativo ou conceitual correto;
- aplicação ao caso concreto;
- organização e progressão da resposta;
- quantidade de erros de língua portuguesa;
- nota estimada pela fórmula do edital.

## Matriz inicial de peças

1. Auditoria do planejamento de uma contratação de solução em nuvem: DFD, ETP, riscos, TR, pesquisa de preços e responsabilidades.
2. Parecer sobre contratação direta de solução proprietária de IA: inexigibilidade, justificativa técnica, preços, riscos, LGPD, explicabilidade e dependência do fornecedor.
3. Relatório de incidente com credenciais comprometidas: ITIL 4, resposta a incidentes, MFA, IAM, RBAC/ABAC, logs e continuidade.
4. Nota técnica para plataforma analítica de combate a fraude: qualidade dos dados, ETL/ELT, data lake, modelos, métricas, viés e governança.
5. Parecer de modernização de sistema legado: microsserviços, APIs, eventos, testes, CI/CD, segurança, observabilidade e estratégia de migração.

## Conclusão operacional

Para a discursiva, a prioridade não deve copiar mecanicamente o ranking da objetiva. Contratações de TI assume o primeiro lugar pela repetição nas peças. Governança e segurança vêm em seguida. IA, dados e arquitetura devem ser estudados de forma integrada porque os casos mais recentes cobram aplicação no setor público, riscos e tomada de decisão, e não definições isoladas.

## Fontes oficiais

- [Edital do TCE-MA — Cargo 10](../documentos%20de%20apoio/tce-edital.pdf)
- [TCE-RJ — padrão definitivo completo da discursiva de TI](https://cdn.cebraspe.org.br/concursos/tce_rj_20/arquivos/TCE_RJ_20_PADRAO_DE_RESPOSTAS_DEFINITIVO_CARGO_04_COMPLETO.PDF)
- [TCDF — prova discursiva da especialidade de infraestrutura de TI](https://cdn.cebraspe.org.br/concursos/tc_df_24_auditor/arquivos/TCDF_AUDITOR_PROVA_DISCURSIVA__ESPECIALIDADE_3.PDF)
- [TCDF — padrão definitivo de respostas](https://cdn.cebraspe.org.br/concursos/tc_df_24_auditor/arquivos/PADRO_DEFINITIVO_DE_RESPOSTAS___PROVA_DISCURSIVA__ESPECIALIDADE_3.PDF)
- [TCE-PR — padrão definitivo da discursiva de Informática](https://cdn.cebraspe.org.br/concursos/tce_pr_24_auditor/arquivos/TCEPR_PADRO_DEFINITIVO_DE_RESPOSTAS_CARGO_5.PDF)
- [TCE-MS — padrão definitivo de respostas de TI](https://cdn.cebraspe.org.br/concursos/tce_ms_25/arquivos/737DF8925BAB03880ECC1029ABB1F3CCFD17897262638E79E1D5466427410693.pdf)
- [TCE-RN — padrão de resposta de Segurança da Informação](https://cdn.cebraspe.org.br/concursos/tce_rn_25/arquivos/A4A95EA22A5DD7C0CC1A241F29E10BE9D56549296FAE18D5913AA25A2D1B6F18.pdf)

## Limitações

- Foram contados apenas itens técnicos localizados com segurança em documentos oficiais.
- Especialidades e editais anteriores não são idênticos ao Cargo 10 do TCE-MA.
- O histórico informa o tipo de caso que a banca já cobrou, mas não permite prever o tema exato da prova.
- A redação das normas deve ser revisada na versão vigente próxima à prova.
