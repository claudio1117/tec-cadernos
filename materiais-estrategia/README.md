# Materiais Estratégia

Automação independente para catalogar, baixar e preparar os PDFs que a conta
autenticada do usuário pode obter normalmente no Estratégia
Concursos. Este projeto não compartilha código interno, perfil do navegador ou
estado de execução com `cadernos-tec`.

O projeto já implementa a fundação do navegador, detecção básica de sessão,
catálogo de matrículas, inventário de pacotes e download retomável dos livros
eletrônicos que a própria página de cada aula disponibiliza. O Chrome usa perfil
persistente exclusivo e expõe o Chrome DevTools Protocol (CDP) apenas no
localhost.

Uma etapa local e separada valida os downloads, extrai o texto dos PDFs e
publica JSONs estruturados para integrações futuras.

## Limites de uso

A automação será operada somente sobre a sessão e os materiais aos quais o
usuário já possui acesso legítimo. Não haverá tentativa de contornar CAPTCHA,
DRM, paywall, expiração de sessão ou qualquer outro controle de acesso. Quando
houver uma etapa de autenticação ou desafio interativo, ela será concluída
manualmente no navegador.

## O que foi aproveitado conceitualmente de `cadernos-tec`

A análise do projeto irmão identificou padrões úteis, sem copiar estado ou
incorporar código específico do TEC:

- navegador visível e autenticação manual, com automação posterior sobre a mesma
  sessão;
- perfil persistente exclusivo, mantido fora do Git;
- CDP como fronteira entre o Python e a página já autenticada;
- scripts pequenos, executáveis pela linha de comando e baseados inicialmente na
  biblioteca padrão do Python;
- configuração por argumentos e variáveis de ambiente;
- operações de leitura/validação antes das operações que alteram estado;
- resultados JSON incrementais e retomáveis, com URLs e identificadores de
  origem preservados;
- separação entre código, planos/configurações, dados coletados e resultados.

O cliente CDP do TEC também resolve WebSocket sem dependências externas e possui
uma ponte PowerShell para Chrome do Windows acessado pelo WSL em modo NAT. Esses
dois componentes são boas referências, mas só devem ser adaptados aqui se a
investigação do Estratégia exigir avaliação de DOM ou chamadas CDP a partir do
WSL. Seletores, rotas, serviços Angular e regras do TEC não são reutilizáveis.

## Estrutura atual

```text
materiais-estrategia/
├── .chrome-estrategia-profile/   # criado no primeiro start; ignorado pelo Git
├── config/
│   └── settings.example.json     # contrato inicial de configuração
├── data/
│   ├── catalogs/                 # inventários intermediários, locais
│   ├── manifests/                # manifestos brutos do downloader, locais
│   └── processados/              # manifesto, índice e relatório derivados
├── downloads/                    # PDFs baixados, locais
├── estrategia/                   # pacote e CLI de processamento local
├── examples/
│   ├── manifest.example.json
│   └── processed-manifest.example.json
├── scripts/
│   ├── estrategia_browser.py     # launcher e diagnóstico HTTP do CDP
│   ├── estrategia_cdp.py         # inspeção da sessão e catálogo de matrículas
│   └── estrategia_materials.py   # inventário e download retomável dos PDFs
├── textos/                       # textos derivados, locais
├── tests/                        # testes da etapa de processamento
├── .gitignore
└── README.md
```

Os diretórios de dados e downloads estão ignorados por padrão porque podem
revelar informações da conta e conter material protegido. Os arquivos
`.gitkeep` preservam apenas a estrutura vazia.

## Requisitos

- Python 3.10 ou mais recente;
- Google Chrome ou Chromium disponível no sistema;
- `pdftotext` do Poppler (`poppler-utils` em Debian/Ubuntu), para a etapa de
  extração;
- acesso legítimo a uma conta do Estratégia Concursos.

O perfil e a porta são diferentes dos usados pelo TEC:

| Projeto | Perfil padrão | Porta CDP |
| --- | --- | ---: |
| `cadernos-tec` | `.chrome-tec-profile/` | `9222` |
| `materiais-estrategia` | `.chrome-estrategia-profile/` | `9223` |

## Iniciar o navegador

Na raiz deste projeto:

```bash
python3 scripts/estrategia_browser.py start
```

O comando localiza `google-chrome` ou `chromium`, cria o perfil exclusivo,
inicia a página pública do Estratégia e espera o endpoint CDP responder. Faça o
login manualmente nessa janela quando necessário. Cookies e demais dados da
sessão permanecerão em `.chrome-estrategia-profile/` para as execuções seguintes.

Em terminais ou ambientes que encerram processos filhos quando o comando
principal termina, mantenha o launcher em primeiro plano até fechar o Chrome:

```bash
python3 scripts/estrategia_browser.py start --wait
```

Para conferir o comando sem abrir uma janela:

```bash
python3 scripts/estrategia_browser.py start --dry-run
```

Para confirmar que o Chrome está acessível e listar as abas expostas pelo CDP:

```bash
python3 scripts/estrategia_browser.py status
```

Com a sessão autenticada e a página **Minhas Matrículas** aberta, liste os cursos
com identificador, URL e período de disponibilidade:

```bash
python3 scripts/estrategia_cdp.py courses
```

Para preservar um snapshot local do catálogo:

```bash
python3 scripts/estrategia_cdp.py \
  --output data/catalogs/cursos-matriculados.json \
  courses
```

Essa operação somente lê os cartões já renderizados na página; ela não abre um
curso nem inicia downloads.

### Inventariar e baixar um pacote

Primeiro salve os cursos e aulas componentes do pacote:

```bash
python3 scripts/estrategia_materials.py inventory ID_DO_PACOTE \
  --output data/catalogs/inventario-do-pacote.json
```

Depois baixe os livros eletrônicos e mantenha um manifesto incremental:

```bash
python3 scripts/estrategia_materials.py download \
  data/catalogs/inventario-do-pacote.json \
  --manifest data/manifests/manifesto-do-pacote.json \
  --download-dir downloads/pacote
```

O processo valida a assinatura `%PDF`, registra tamanho e SHA-256 e pula arquivos
já confirmados em uma retomada. `--lesson-id ID` restringe a execução a uma aula
específica. O fluxo baixa as variantes de **Livro Eletrônico** expostas na aula;
slides e vídeos não são incluídos.

## Processar os materiais baixados

Esta etapa não usa o Chrome e não altera os PDFs. Na raiz do projeto, execute:

```bash
python3 -m estrategia processar-materiais
```

Quando existe um único JSON válido em `data/manifests/`, ele é selecionado
automaticamente. Se houver vários, indique o desejado explicitamente:

```bash
python3 -m estrategia processar-materiais \
  --manifesto-fonte data/manifests/meu-curso.json
```

Para uma prova pequena antes de processar o acervo inteiro:

```bash
python3 -m estrategia processar-materiais --limite 3
```

O comando produz:

```text
data/processados/<curso>/manifesto.json  # metadados verificados e estado por PDF
data/processados/<curso>/indice.json     # curso > disciplinas > aulas > materiais
data/processados/<curso>/relatorio.json  # contadores, validação e erros da execução
textos/<curso>/<disciplina>/<aula>/<material>.txt
```

Em cada execução, o processador recalcula o SHA-256 e o tamanho do PDF. Uma
extração somente é ignorada quando o hash atual coincide com o registrado e o
texto correspondente ainda existe com o tamanho esperado. `--forcar` refaz tudo.
Uma falha individual é registrada no manifesto e no relatório, sem impedir os
demais PDFs; nesse caso, o comando termina com código diferente de zero.

O manifesto bruto existente não possui o nome retornado originalmente pelo
servidor. Por isso, o contrato processado usa o nome local como fallback e marca
`nome_original_confirmado: false`. Downloads futuros podem preencher
`nome_original` no manifesto bruto, caso o downloader passe a preservar esse
dado; nenhuma suposição é apresentada como nome confirmado.

É possível escolher outro binário ou porta:

```bash
python3 scripts/estrategia_browser.py --port 9323 start --browser /caminho/chrome
```

As variáveis `ESTRATEGIA_CHROME_BINARY`, `ESTRATEGIA_DEBUG_HOST`,
`ESTRATEGIA_DEBUG_PORT` e `ESTRATEGIA_START_URL` oferecem as mesmas substituições.
Por segurança, o launcher rejeita um host CDP que não seja local. Uma porta CDP
dá controle amplo sobre o navegador autenticado e não deve ser publicada na
rede.

### WSL com Chrome do Windows

O launcher atual usa um Chrome disponível no mesmo ambiente do Python. Se for
necessário controlar o Chrome do Windows a partir de WSL em modo NAT, a próxima
etapa deve adaptar a ponte por entrada/saída padrão já validada em
`cadernos-tec`, mantendo nomes, porta e perfil exclusivos do Estratégia. Não se
deve apontar esta automação para o perfil do TEC.

## Arquitetura

A evolução será dividida por responsabilidades, mantendo detalhes da plataforma
fora do navegador e do armazenamento:

```text
Chrome + perfil próprio
        │ CDP
        ▼
browser/cdp ──► estrategia/auth
                       │
                       ▼
                estrategia/catalog
                       │
              cursos → disciplinas → aulas → materiais
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
       storage/catalog      downloads/worker
                                  │
                                  ▼
                           storage/manifest
                                  │
                                  ▼
                         processing/textos
                                  │
                                  ▼
                       manifesto + índice + relatório
```

- `browser/cdp`: conexão, navegação, espera por carregamento e avaliação segura
  no contexto da página;
- `estrategia/auth`: detecção de estado autenticado, sem automatizar credenciais
  ou desafios;
- `estrategia/catalog`: descoberta de cursos, disciplinas, aulas e PDFs, usando
  apenas rotas e elementos observados na sessão do usuário;
- `downloads/worker`: download posterior pelos mecanismos normais oferecidos
  pela plataforma, com validação de nome, tipo, tamanho e conclusão;
- `storage/catalog`: snapshots de descoberta que permitam revisão humana antes
  de qualquer download;
- `storage/manifest`: escrita validada e incremental do registro bruto dos
  downloads;
- `processing/textos`: verifica os arquivos locais por hash e extrai texto sem
  alterar os PDFs;
- `manifesto + índice + relatório`: contrato de intercâmbio que não expõe os
  detalhes internos da automação.

A automação de navegador e o downloader permanecem em scripts separados. O
pacote `estrategia` cuida apenas do processamento local e dos contratos de saída.

## Fluxo funcional

1. Abrir o Chrome dedicado e permitir login manual.
2. Detectar de forma somente leitura se a sessão está autenticada.
3. Listar cursos e salvar um snapshot do catálogo.
4. Selecionar um curso por identificador estável, nunca apenas pela posição na
   tela.
5. Listar disciplinas, aulas e materiais disponíveis.
6. Gerar um plano revisável dos PDFs encontrados.
7. Baixar os arquivos selecionados e atualizar o manifesto bruto de forma
   incremental.
8. Validar os PDFs locais, extrair textos e publicar manifesto processado,
   índice e relatório.

Falhas de autenticação, CAPTCHA ou ausência de permissão interromperão o fluxo e
serão encaminhadas para resolução manual.

## Contratos de dados

O manifesto bruto do downloader é exemplificado por
`examples/manifest.example.json`. O manifesto derivado está exemplificado por
`examples/processed-manifest.example.json`. `schema_version` permite evolução
compatível, e os caminhos ficam relativos à raiz do projeto quando os artefatos
estão dentro dela.

Uma versão inicial terá a forma:

```json
{
  "schema_version": 1,
  "curso": "...",
  "materiais": [
    {
      "disciplina": "...",
      "aula": "...",
      "titulo": "...",
      "caminho_pdf": "downloads/...pdf",
      "nome_original": "arquivo.pdf",
      "nome_original_confirmado": false,
      "url_origem": "...",
      "baixado_em": "...",
      "tamanho_bytes": 123,
      "sha256": "...",
      "extracao": {
        "status": "ok",
        "pdf_sha256": "...",
        "texto": "textos/...txt"
      }
    }
  ]
}
```

Datas usam ISO 8601 com fuso horário. O `indice.json` é a interface preferencial
para navegação: agrupa disciplinas, aulas e, em cada aula, os caminhos do PDF e
do texto correspondente.

## Integração futura com `cadernos-tec`

A integração ocorrerá somente pelos JSONs versionados e arquivos neles
referenciados. `cadernos-tec` poderá ler `indice.json`, metadados, PDFs ou textos
publicados por este projeto, mas não importará módulos internos, compartilhará
cookies nem reutilizará o perfil do Chrome. Uma eventual mudança de interface do
Estratégia ficará assim isolada neste projeto.

## Próximas evoluções

- testes automatizados sobre snapshots sanitizados da interface;
- validação formal do manifesto por JSON Schema;
- relatório de diferenças quando um curso adicionar ou substituir aulas;
- política configurável para variantes de PDF.
