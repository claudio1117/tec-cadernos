# Estado atual do projeto

Última atualização: 21/09/2026.

## Situação

O planejamento inicial foi concluído e os oito cadernos do primeiro dia foram criados no Tec Concursos. Eles totalizam 60 questões: 15 de conhecimentos gerais e 45 de conhecimentos específicos.

As URLs, quantidades e modalidades estão registradas em `planos/2026-09-21-resultados.md`. O arquivo `planos/2026-09-21-plano-executado.json` é um registro histórico da entrada usada na automação e não deve ser executado novamente.

## Trabalho já concluído

- Escopo e regras permanentes registrados em `AGENTS.md`.
- Edital oficial preservado em `documentos de apoio/tce-edital.pdf`.
- Análise de incidência da prova objetiva concluída.
- Análise separada da prova discursiva concluída.
- Matriz inicial de prioridade criada.
- Cadernos D01-G01 a D01-E05 criados.
- Expansão do bloco D01-E04 para Cebraspe Certo ou Errado registrada por insuficiência de múltipla escolha.

## Pendência atual

Resolver e corrigir os cadernos do primeiro dia. Ainda não foram fornecidos ou registrados:

- resultados por bloco;
- questões erradas ou duvidosas;
- níveis de confiança;
- diagnósticos de erro;
- revisões ou retestes agendados.

Até esses dados existirem, não presumir domínio, dificuldade individual nem histórico de desempenho.

## Próximo passo

1. O aluno resolve os cadernos listados em `planos/2026-09-21-resultados.md`.
2. Para cada erro ou dúvida, informa a questão e a confiança 1, 2 ou 3.
3. O tutor registra somente `Regra correta | Conceito confundido | Mecanismo do distrator`.
4. O tutor agenda os retestes conforme `AGENTS.md`.
5. Somente depois disso é preparado o próximo ciclo diário, priorizando erros, retestes e revisões antes de conteúdo novo.

## Dependências externas

- Os cadernos pertencem à conta do aluno no Tec Concursos; as URLs não substituem a autenticação.
- Em uma nova máquina, é necessário entrar novamente nessa conta.
- Para usar a automação, seguir as instruções do `README.md` e manter a pasta de destino do Tec com o nome exato esperado pelo script.
- O caderno incorreto `103891781` foi movido para “Cadernos excluídos” durante o desenvolvimento da automação. Ele não faz parte do plano e não deve ser restaurado.

