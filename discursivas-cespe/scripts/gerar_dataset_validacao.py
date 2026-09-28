#!/usr/bin/env python3
"""Gera os CSVs da validação inicial a partir dos 3 concursos selecionados.

Os enunciados foram transcritos dos cadernos oficiais. A seção expositiva de cada
padrão definitivo é extraída dos PDFs locais entre os marcadores do próprio documento;
as tabelas de critérios/"quesitos avaliados" permanecem preservadas nos PDFs-fonte.
"""

from __future__ import annotations

import csv
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def compact(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def json_list(*values: str) -> str:
    return json.dumps(list(values), ensure_ascii=False)


def extract_patterns(pdf: Path) -> list[str]:
    result = subprocess.run(
        ["pdftotext", "-layout", str(pdf), "-"],
        check=True,
        capture_output=True,
        text=True,
    )
    patterns = re.findall(
        r"PADRÃO DE RESPOSTA DEFINITIVO\s*(.*?)\s*QUESITOS AVALIADOS",
        result.stdout,
        flags=re.DOTALL,
    )
    return [compact(item.replace("\f", " ")) for item in patterns]


URLS = {
    "rj_edital": "https://cdn.cebraspe.org.br/concursos/tce_rj_20/arquivos/ED_1_2020_TCE_RJ_ABERTURA.PDF",
    "rj_prova": "https://cdn.cebraspe.org.br/concursos/tce_rj_20/arquivos/CARGO_4_DISCURSIVA.PDF",
    "rj_padrao": "https://cdn.cebraspe.org.br/concursos/tce_rj_20/arquivos/TCE_RJ_20_PADRAO_DE_RESPOSTAS_DEFINITIVO_CARGO_04_COMPLETO.PDF",
    "df_edital": "https://cdn.cebraspe.org.br/concursos/tc_df_24_auditor/arquivos/ED_1_TCDF_ACE_ABERTURA_VERSAO_COMPILADA_ATE_RET_ED_2.PDF",
    "df_prova": "https://cdn.cebraspe.org.br/concursos/tc_df_24_auditor/arquivos/TCDF_AUDITOR_PROVA_DISCURSIVA__ESPECIALIDADE_3.PDF",
    "df_padrao": "https://cdn.cebraspe.org.br/concursos/tc_df_24_auditor/arquivos/PADRO_DEFINITIVO_DE_RESPOSTAS___PROVA_DISCURSIVA__ESPECIALIDADE_3.PDF",
    "ms_edital": "https://cdn.cebraspe.org.br/concursos/tce_ms_25/arquivos/84E86AED6CE1736C8A0CBD0840FAB66E40C05BDF0B76ACD4DC0F5D4FE0A8B5C7.pdf",
    "ms_prova": "https://cdn.cebraspe.org.br/concursos/tce_ms_25/arquivos/9D84E7DA00CB1E6420C5FA623DFD21125CAE15D164C982C05536423237BFC1BC.pdf",
    "ms_padrao": "https://cdn.cebraspe.org.br/concursos/tce_ms_25/arquivos/737DF8925BAB03880ECC1029ABB1F3CCFD17897262638E79E1D5466427410693.pdf",
}


CONCURSOS = [
    {
        "id_concurso": "tce_rj_2021_ace_ti",
        "ano": 2021,
        "orgao": "Tribunal de Contas do Estado do Rio de Janeiro (TCE/RJ)",
        "cargo": "Analista de Controle Externo – Área: Controle Externo",
        "especialidade": "Tecnologia da Informação",
        "banca": "CEBRASPE",
        "tipo_orgao": "Tribunal de Contas estadual",
        "nivel_cargo": "superior",
        "categoria_comparabilidade": "A",
        "url_edital": URLS["rj_edital"],
        "url_prova": URLS["rj_prova"],
        "url_padrao_resposta": URLS["rj_padrao"],
        "fonte_oficial": "sim — cdn.cebraspe.org.br",
        "status_confirmacao": "confirmado",
        "observacoes": "Edital publicado em 2020; prova aplicada em 7/2/2021. Cargo 4 confirmado no edital, no caderno discursivo e no padrão definitivo.",
    },
    {
        "id_concurso": "tcdf_2024_ace_ti_infra",
        "ano": 2024,
        "orgao": "Tribunal de Contas do Distrito Federal (TCDF)",
        "cargo": "Auditor de Controle Externo – Área Especializada",
        "especialidade": "Tecnologia da Informação – Orientação Microinformática e Infraestrutura de TI",
        "banca": "CEBRASPE",
        "tipo_orgao": "Tribunal de Contas distrital",
        "nivel_cargo": "superior",
        "categoria_comparabilidade": "A",
        "url_edital": URLS["df_edital"],
        "url_prova": URLS["df_prova"],
        "url_padrao_resposta": URLS["df_padrao"],
        "fonte_oficial": "sim — cdn.cebraspe.org.br",
        "status_confirmacao": "confirmado",
        "observacoes": "Especialidade 3; prova aplicada em 17/11/2024. Cargo, orientação e nível superior confirmados no edital e nos documentos da prova.",
    },
    {
        "id_concurso": "tce_ms_2025_ace_ti",
        "ano": 2025,
        "orgao": "Tribunal de Contas do Estado de Mato Grosso do Sul (TCE/MS)",
        "cargo": "Auditor de Controle Externo",
        "especialidade": "Área: Tecnologia da Informação",
        "banca": "CEBRASPE",
        "tipo_orgao": "Tribunal de Contas estadual",
        "nivel_cargo": "superior",
        "categoria_comparabilidade": "A",
        "url_edital": URLS["ms_edital"],
        "url_prova": URLS["ms_prova"],
        "url_padrao_resposta": URLS["ms_padrao"],
        "fonte_oficial": "sim — cdn.cebraspe.org.br",
        "status_confirmacao": "confirmado",
        "observacoes": "Cargo 5; prova aplicada em 26/10/2025. O cabeçalho da Questão 2 no padrão definitivo informa 25/10/2025, divergindo do caderno e das demais questões; foi adotada a data do caderno.",
    },
]


def base_question(
    *, qid: str, contest: dict[str, object], kind: str, lines: int, points: float,
    statement: str, required: tuple[str, ...], theme: str, subthemes: tuple[str, ...],
    situation: str, citations: tuple[str, ...], scope: str, match: str,
    mapped_items: tuple[str, ...], pattern: str, proof_url: str, answer_url: str,
    source_statement: str, source_answer: str, notes: str = "",
) -> dict[str, object]:
    return {
        "id_questao": qid,
        "id_concurso": contest["id_concurso"],
        "ano": contest["ano"],
        "orgao": contest["orgao"],
        "cargo": contest["cargo"],
        "especialidade": contest["especialidade"],
        "tipo_discursiva": kind,
        "numero_maximo_linhas": lines,
        "pontuacao": f"{points:.2f}".replace(".", ","),
        "enunciado_integral": compact(statement),
        "itens_exigidos": json_list(*required),
        "tema_principal": theme,
        "subtemas": json_list(*subthemes),
        "situacao_problema": situation,
        "norma_ou_tecnologia_citada": json_list(*citations),
        "conhecimento_geral_ou_especifico": scope,
        "correspondencia_com_edital_tce_ma": match,
        "itens_correspondentes_tce_ma": json_list(*mapped_items),
        "texto_padrao_resposta": pattern,
        "url_prova": proof_url,
        "url_padrao_resposta": answer_url,
        "fonte_enunciado": source_statement,
        "fonte_padrao_resposta": source_answer,
        "status_confirmacao": "confirmado",
        "observacoes": notes,
    }


def build_questions() -> list[dict[str, object]]:
    rj, df, ms = CONCURSOS
    rj_patterns = extract_patterns(ROOT / "fontes/padroes_resposta/tce_rj_2021_cargo4_padrao_definitivo.pdf")
    df_patterns = extract_patterns(ROOT / "fontes/padroes_resposta/tcdf_2024_especialidade3_padrao_definitivo.pdf")
    ms_patterns = extract_patterns(ROOT / "fontes/padroes_resposta/tce_ms_2025_cargo5_padrao_definitivo.pdf")
    if [len(rj_patterns), len(df_patterns), len(ms_patterns)] != [4, 3, 4]:
        raise RuntimeError("Quantidade inesperada de padrões de resposta extraídos")

    rows: list[dict[str, object]] = []
    rows.append(base_question(
        qid="tce_rj_2021_ace_ti_q1", contest=rj, kind="questão dissertativa", lines=20, points=20,
        statement="""
        As contas de um gestor público da Secretaria de Estado de Saúde do Estado do Rio de Janeiro (SES/RJ) foram julgadas irregulares pelo Tribunal de Contas do Estado do Rio de Janeiro (TCE/RJ), por ele ter dispensado, fora dos casos previstos em lei, licitação para aquisição de medicamentos. O gestor alegou que o julgamento foi totalmente desconexo da realidade, uma vez que era patente a situação de emergência, e que, em nenhum momento, ele fora chamado para apresentar sua defesa. Considerando a situação hipotética apresentada, redija um texto atendendo ao que se pede a seguir. 1 Identifique o tipo de decisão adotada pelo TCE/RJ no caso em apreço. [valor: 2,00 pontos] 2 Discorra sobre os recursos cabíveis para contestar a decisão do TCE/RJ [valor: 6,00 pontos], indicando o prazo para sua interposição [valor: 1,50 ponto] e como se dá sua contagem [valor: 2,00 pontos], bem como os efeitos desses recursos quando de seu recebimento [valor: 1,50 ponto]. 3 Esclareça se há possibilidade de a decisão ser modificada ou anulada pelo Poder Judiciário. [valor: 6,00 pontos]
        """,
        required=("tipo de decisão do TCE/RJ", "recursos cabíveis, prazos, contagem e efeitos", "possibilidade e limites de controle judicial"),
        theme="Controle externo e recursos contra decisão de tribunal de contas",
        subthemes=("decisão definitiva", "embargos de declaração", "recurso de reconsideração", "recurso de revisão", "controle judicial"),
        situation="Contas julgadas irregulares por dispensa de licitação; gestor alega emergência e ausência de defesa.",
        citations=("Lei Orgânica do TCE/RJ",), scope="geral", match="inexistente", mapped_items=(), pattern=rj_patterns[0],
        proof_url=URLS["rj_prova"], answer_url=URLS["rj_padrao"], source_statement="caderno oficial, PDF p. 2", source_answer="padrão definitivo, PDF pp. 1–2",
        notes="Questão geral efetivamente integrante da prova do cargo de TI; não há item equivalente no conteúdo específico do Cargo 10 do TCE-MA.",
    ))
    rows.append(base_question(
        qid="tce_rj_2021_ace_ti_q2", contest=rj, kind="questão dissertativa", lines=20, points=20,
        statement="""
        A mineração de regras de associação é um método comumente usado para explicar o que é a mineração de dados e o que ela é capaz de fazer. Como exemplo, tem-se o clássico caso de uma grande rede de supermercados norte-americana que, a partir de uma análise dos hábitos de compras dos clientes, descobriu uma relação estatística entre compras de cerveja e compras de fraldas. Entendeu-se, assim, que o motivo dessa associação era que os pais (presumidamente homens jovens), ao irem comprar fraldas para seus bebês (sobretudo às quintas-feiras), aproveitavam e compravam cervejas para assistir aos jogos de futebol em casa, uma vez que já não poderiam ir aos jogos com a mesma frequência de antes. O resultado disso foi que a rede de supermercados passou a oferecer um display de cervejas ao lado das fraldas para facilitar o consumo casado desses produtos. Considerando que o fragmento de texto precedente tem caráter unicamente motivador, redija um texto dissertativo atendendo ao que se pede a seguir. 1 Explique por que as regras de associação em mineração de dados são úteis para a análise da relação entre um item e outro, ainda que aparentemente desconexos. [valor: 6,00 pontos] 2 Apresente um exemplo de contexto potencial de negócios para aplicação das regras de associação para mineração de dados e descreva dois dados que podem ser identificados nesse contexto. [valor: 10,00 pontos] 3 Descreva uma técnica ou um algoritmo que pode ser utilizado para a aplicação de uma regra de associação de mineração de dados. [valor: 3,00 pontos]
        """,
        required=("utilidade das regras de associação", "contexto de negócio e dois dados identificáveis", "técnica ou algoritmo de regras de associação"),
        theme="Mineração de dados — regras de associação",
        subthemes=("análise de cesta de mercado", "suporte", "confiança", "lift", "Apriori", "Eclat", "FP-Growth"),
        situation="Associação entre itens de compra usada para decisões comerciais.", citations=("mineração de dados", "Apriori", "Eclat", "FP-Growth"),
        scope="específico", match="direta", mapped_items=("ANÁLISE DE DADOS — 3 Mineração de dados.", "ANÁLISE DE DADOS — 3.3 Técnicas e tarefas de mineração de dados.", "ANÁLISE DE DADOS — 3.5 Regras de associação."),
        pattern=rj_patterns[1], proof_url=URLS["rj_prova"], answer_url=URLS["rj_padrao"], source_statement="caderno oficial, PDF p. 3", source_answer="padrão definitivo, PDF pp. 3–4",
    ))
    rows.append(base_question(
        qid="tce_rj_2021_ace_ti_q3", contest=rj, kind="questão dissertativa", lines=20, points=20,
        statement="""
        O conceito de BYOD — do inglês, bring your own device, que significa “traga seu próprio dispositivo” — surge com a explosão do mundo mobile: a ideia é dar liberdade ao funcionário para que ele possa usar seus próprios aparelhos e dispositivos para acessar e modificar informações da empresa. Com a comodidade de utilizar computadores ou smartphones que lhe convêm, o empregado consegue cuidar de questões importantes de qualquer lugar. O processo de implementação do BYOD, no entanto, não é simples. Empresas que adotam essa solução precisam preocupar-se com uma gama de questões relativas a segurança e flexibilidade. O desafio é encontrar o equilíbrio entre um ambiente extremamente seguro e a capacidade de permitir que os funcionários acessem os dados de diversas e simplificadas formas. Internet: <https://exame.abril.com.br> (com adaptações). Considerando que o fragmento de texto anterior tem caráter unicamente motivador, redija um texto dissertativo acerca dos requisitos para a garantia da segurança da informação em organizações que permitam o trabalho remoto a partir de dispositivos móveis pessoais de funcionários. Em seu texto, atenda ao que se pede a seguir. 1 Discorra sobre a relação entre a prática do BYOD e a necessidade de implementação de uma política de segurança da informação, explicando como os usuários devem considerar termos de uso da empresa ou do órgão público e como o uso de software para controle remoto do dispositivo pessoal pode alterar configurações de segurança do dispositivo pessoal. [valor: 6,00 pontos] 2 Apresente, pelo menos, três medidas de segurança para acesso remoto a dados nesse contexto, em que a informação não é necessariamente classificada. [valor: 6,50 pontos] 3 Aborde, pelo menos, três medidas de segurança avançadas a serem adotadas caso o funcionário tenha acesso a informação classificada. [valor: 6,50 pontos]
        """,
        required=("BYOD, política de segurança, termos de uso e controle remoto", "três medidas para acesso remoto a dados não classificados", "três medidas avançadas para informação classificada"),
        theme="Segurança da informação em BYOD",
        subthemes=("política de segurança", "acesso remoto", "MDM", "VPN", "autenticação multifator", "certificados digitais", "controle de acesso"),
        situation="Uso de dispositivos móveis pessoais para acesso remoto a informações organizacionais.",
        citations=("BYOD", "MDM", "VPN", "CAPTCHA", "biometria", "certificados digitais"), scope="específico", match="parcial",
        mapped_items=("GESTÃO E GOVERNANÇA DE TI — 10 Cibersegurança e continuidade de negócios (ISO 27001/22301, 27002, NIST).", "ARQUITETURA DE SOFTWARE — 16 Arquitetura de soluções mobile.", "ARQUITETURA DE SOFTWARE — 18 Autenticação única (single sign‐on)."),
        pattern=rj_patterns[2], proof_url=URLS["rj_prova"], answer_url=URLS["rj_padrao"], source_statement="caderno oficial, PDF p. 4", source_answer="padrão definitivo, PDF p. 5",
        notes="Correspondência parcial: o edital do TCE-MA cobre cibersegurança de modo amplo e soluções mobile, mas não explicita BYOD/MDM nem o recorte de informação classificada.",
    ))
    rows.append(base_question(
        qid="tce_rj_2021_ace_ti_peca", contest=rj, kind="peça de natureza técnica — parecer", lines=50, points=40,
        statement="""
        RELATÓRIO DE AUDITORIA N.º 1/2020. Trata-se de auditoria interna realizada por servidores do órgão XPTO no exercício de 2020, em atendimento ao plano de auditoria e em observância às orientações da legislação em vigor. Considerando os achados de auditoria relatados, relacionados às contratações de soluções de tecnologia da informação e comunicação (TIC) no presente órgão, integrante do Sistema de Administração dos Recursos de Tecnologia da Informação (SISP), servimo-nos do presente relatório para informar que foi constatado e analisado o seguinte. I No rito da contratação n.º 10, o gerenciamento de risco foi realizado a partir da fase de seleção do fornecedor. Tal procedimento é justificado, pois o gerenciamento de riscos deve ser executado até essa fase. O seguimento para as demais fases de contratação deve acontecer tão somente no caso de o resultado da análise de risco ter sido favorável e, neste caso, deve-se realizar, na fase de seleção do fornecedor, o estudo técnico preliminar da contratação. II Não foram encontradas inconsistências no rito da contratação n.º 20. A licitação foi corretamente classificada como inexigível, de acordo com a Lei n.º 8.666/1993, pois o objeto da contratação é fornecido por empresa exclusiva. Por conseguinte, devido à inexigibilidade, não se fez necessário elaborar termo de referência nem estudo técnico preliminar da contratação. III Não foram encontradas inconsistências na gestão do contrato n.º 30. O fiscal identificou que o objeto do contrato, referente à prestação de serviços executados de forma contínua, teve sua prorrogação cancelada após transcorridos doze meses contados da sua data de vigência. A justificativa que embasa tal procedimento é que contratos devem ser obrigatoriamente adstritos à vigência dos respectivos créditos orçamentários e limitados a doze meses. IV No rito da contratação n.º 40, foi identificado que a definição e a especificação das necessidades tecnológicas e dos requisitos necessários foram inseridos no documento de oficialização da demanda (DOD), elaborado exclusivamente pelo integrante técnico. Ainda que o conteúdo do DOD esteja de acordo com a legislação, esse documento deveria ter sido elaborado pelo integrante requisitante. V No rito da contratação n.º 50, foi identificado que a equipe de planejamento da contratação era composta pela autoridade máxima da área de TIC juntamente com um integrante técnico e outro administrativo, tendo os três assinado e aprovado o estudo técnico preliminar da contratação. Nesse caso, houve uma divergência com a legislação, que veda que o integrante administrativo e a autoridade máxima da área de TIC façam parte da equipe de planejamento e assinem o referido estudo. VI Não foram encontradas inconsistências no rito da contratação n.º 60. Foi utilizada a modalidade pregão, regida pela Lei n.º 10.520/2002, tendo sido sequencialmente realizadas as seguintes ações: a) verificação, pelo pregoeiro, dos documentos de habilitação do licitante, de acordo com as condições fixadas no edital; b) exame da melhor proposta sob o critério de técnica e preço; e, por fim, c) realização da adjudicação do objeto da licitação ao licitante vencedor. Assim sendo, solicitamos sua manifestação por meio de um parecer técnico no sentido de apresentar esclarecimentos, justificativas ou providências, no prazo de cinco dias úteis, contados do recebimento deste. Atenciosamente, Coordenador da Equipe de Auditoria Interna do Órgão XPTO. Com base nas informações constantes do relatório de auditoria n.º 1/2020, apresentado anteriormente, redija, na condição de analista de controle externo, um parecer técnico avaliando, em sua completude, todos os achados e as análises apresentados pelo coordenador da equipe de auditoria interna do órgão XPTO, esclarecendo se estão ou não de acordo com a legislação em vigor. Em seu parecer, não crie fatos novos e dispense a ementa, o relatório, o local, a data e a assinatura.
        """,
        required=("avaliar o achado I — riscos e ETP", "avaliar o achado II — inexigibilidade e planejamento", "avaliar o achado III — duração de serviço contínuo", "avaliar o achado IV — DOD e requisitos", "avaliar o achado V — equipe e aprovação do ETP", "avaliar o achado VI — pregão, julgamento, habilitação e adjudicação"),
        theme="Auditoria de contratações de soluções de TIC",
        subthemes=("planejamento da contratação", "gerenciamento de riscos", "ETP", "termo de referência", "inexigibilidade", "equipe de planejamento", "pregão"),
        situation="Parecer sobre seis achados de auditoria em contratações de TIC.", citations=("SISP", "IN SGD/ME nº 1/2019", "Lei nº 8.666/1993", "Lei nº 10.520/2002"),
        scope="específico", match="parcial",
        mapped_items=("GESTÃO E GOVERNANÇA DE TI — 2 Gestão de riscos de TI (ISO 31000, COSO).", "GESTÃO E GOVERNANÇA DE TI — 6 Contratações de TI no setor público.", "CONTRATAÇÕES DE TI — 1 Gestão de contratação de soluções de TI.", "CONTRATAÇÕES DE TI — 2 Legislação aplicável à contratação de bens e serviços de TI e suas alterações.", "CONTRATAÇÕES DE TI — 2.1 Lei nº 14.133/2021.", "CONTRATAÇÕES DE TI — 2.2 Instrução Normativa SGD/ME nº 94/2022."),
        pattern=rj_patterns[3], proof_url=URLS["rj_prova"], answer_url=URLS["rj_padrao"], source_statement="caderno oficial, PDF p. 5", source_answer="padrão definitivo, PDF pp. 6–8",
        notes="Correspondência parcial: o conceito de contratação de TI é coberto diretamente, mas a questão aplicou normas então vigentes (IN nº 1/2019, Leis nº 8.666/1993 e nº 10.520/2002), enquanto o TCE-MA explicita Lei nº 14.133/2021 e IN nº 94/2022.",
    ))

    rows.append(base_question(
        qid="tcdf_2024_ace_ti_infra_q1", contest=df, kind="questão dissertativa", lines=20, points=10,
        statement="""
        Durante uma grande promoção de vendas, o site de uma empresa que vende produtos pela Internet apresentou lentidão e ficou indisponível por alguns momentos, o que gerou muitas reclamações dos clientes. A equipe de TI foi acionada imediatamente para resolver os problemas reportados, que foram classificados como questões críticas. Após uma análise inicial, descobriu-se que o aumento inesperado no número de acessos sobrecarregou o banco de dados. O time de TI implementou uma solução temporária, porém o incidente evidenciou a necessidade de uma análise mais aprofundada para evitar novas ocorrências dessa situação. Depois de contornado o problema, a equipe de TI reuniu-se para uma análise detalhada dos eventos ocorridos, com vistas à identificação da sua causa raiz. Durante a reunião, a equipe identificou que o sistema de banco de dados não estava devidamente otimizado para lidar com picos de acesso e que, sem um plano de escalabilidade, a empresa correria o risco de enfrentar novos incidentes semelhantes. A partir dessa análise, foram feitas várias recomendações de mudanças no ambiente de TI, tais como a implementação de um sistema de monitoramento de desempenho mais robusto e melhorias na infraestrutura do banco de dados. Conforme a ITIL v4, quais ações ou eventos ocorridos na situação hipotética apresentada fazem parte do processo de gestão de incidentes [valor: 3,75 pontos] e quais fazem parte do processo de gestão de problemas [valor: 3,75 pontos]? Justifique sua resposta, apresentando as definições de gestão de incidentes [valor: 1,00 ponto] e de gestão de problemas [valor: 1,00 ponto].
        """,
        required=("identificar ações/eventos de gestão de incidentes", "identificar ações/eventos de gestão de problemas", "definir gestão de incidentes", "definir gestão de problemas"),
        theme="Gestão de incidentes e de problemas (ITIL v4)", subthemes=("incidente", "problema", "causa-raiz", "solução de contorno", "monitoramento", "escalabilidade"),
        situation="Indisponibilidade de site por sobrecarga do banco de dados e investigação posterior da causa-raiz.", citations=("ITIL v4",), scope="específico", match="direta",
        mapped_items=("GESTÃO E GOVERNANÇA DE TI — 3 Gestão de serviços de TI (ITIL v4).",), pattern=df_patterns[0],
        proof_url=URLS["df_prova"], answer_url=URLS["df_padrao"], source_statement="caderno oficial, PDF p. 1", source_answer="padrão definitivo, PDF p. 1",
    ))
    rows.append(base_question(
        qid="tcdf_2024_ace_ti_infra_q2", contest=df, kind="questão dissertativa", lines=20, points=10,
        statement="""
        À luz da Instrução Normativa SGD/SEDGG/ME n.º 94/2022, redija texto dissertativo a respeito do procedimento de contratação de um serviço especial de tecnologia da informação (TI) no âmbito de um órgão integrante do Sistema de Administração dos Recursos de Tecnologia da Informação (SISP) do Poder Executivo federal. Ao elaborar o seu texto, atenda ao que se pede a seguir. 1 Cite os integrantes da equipe de planejamento da contratação. [valor: 1,50 ponto] 2 Descreva o perfil de cada um dos integrantes da equipe de planejamento da contratação. [valor: 2,00 pontos] 3 Descreva as etapas da fase do planejamento da contratação. [valor: 3,00 pontos] 4 Apresente o conceito de documento de formalização da demanda. [valor: 1,00 ponto] 5 Mencione, no mínimo, três informações que deverão constar no documento de formalização da demanda. [valor: 2,00 pontos]
        """,
        required=("integrantes da equipe de planejamento", "perfil de cada integrante", "etapas do planejamento", "conceito do documento de formalização da demanda", "três informações do documento de formalização da demanda"),
        theme="Planejamento da contratação de serviço de TI", subthemes=("equipe de planejamento", "ETP", "termo de referência", "documento de formalização da demanda", "SISP"),
        situation="Procedimento de contratação de serviço especial de TI em órgão do SISP.", citations=("IN SGD/SEDGG/ME n.º 94/2022", "SISP"), scope="específico", match="direta",
        mapped_items=("GESTÃO E GOVERNANÇA DE TI — 6 Contratações de TI no setor público.", "CONTRATAÇÕES DE TI — 1 Gestão de contratação de soluções de TI.", "CONTRATAÇÕES DE TI — 2.2 Instrução Normativa SGD/ME nº 94/2022."),
        pattern=df_patterns[1], proof_url=URLS["df_prova"], answer_url=URLS["df_padrao"], source_statement="caderno oficial, PDF p. 3", source_answer="padrão definitivo, PDF pp. 2–3",
        notes="A sigla do órgão emissor aparece como SGD/SEDGG/ME no documento histórico e como SGD/ME no edital do TCE-MA; trata-se da IN nº 94/2022.",
    ))
    rows.append(base_question(
        qid="tcdf_2024_ace_ti_infra_peca", contest=df, kind="peça de natureza técnica — informação", lines=50, points=40,
        statement="""
        Houve um problema na estrutura de rede do TCDF e, diante desse fato, a Presidência do TCDF instou à Secretaria-Geral de Administração (SEGEDAM) que buscasse soluções para o problema. A SEGEDAM, então, solicitou à Divisão de Fiscalização de Tecnologia da Informação (DIFTI), por meio do Memorando n.º 016/24 – SEGEDAM, informações técnicas sobre os dois modelos de rede (OSI e TCP/IP) implantados no órgão. Com base na situação hipotética apresentada, redija, na condição de servidor da DIFTI ocupante do cargo de auditor de controle externo, peça de natureza técnica (informação) em que sejam descritas as camadas dos modelos de rede OSI e TCP/IP. Ao elaborar a peça, atenda à estrutura estabelecida no Manual de Redação Oficial do TCDF (2.ª edição), date a informação no dia de hoje e utilize a letra X para qualquer dado necessário e não especificado na situação hipotética. Não crie fatos novos.
        """,
        required=("estrutura de informação do Manual de Redação Oficial do TCDF", "sete camadas do modelo OSI", "cinco camadas do modelo TCP/IP"),
        theme="Modelos de rede OSI e TCP/IP", subthemes=("camada física", "enlace", "rede", "transporte", "sessão", "apresentação", "aplicação"),
        situation="Informação técnica solicitada após problema na estrutura de rede do TCDF.", citations=("modelo OSI", "modelo TCP/IP", "Manual de Redação Oficial do TCDF — 2.ª edição"),
        scope="específico", match="inexistente", mapped_items=(), pattern=df_patterns[2], proof_url=URLS["df_prova"], answer_url=URLS["df_padrao"], source_statement="caderno oficial, PDF p. 4", source_answer="padrão definitivo, PDF pp. 4–5",
        notes="O Cargo 10 do TCE-MA não lista redes de computadores, TCP/IP ou modelo OSI; não se usou a presença genérica de ‘arquitetura’ para forçar correspondência.",
    ))

    rows.append(base_question(
        qid="tce_ms_2025_ace_ti_q1", contest=ms, kind="questão dissertativa", lines=20, points=15,
        statement="""
        A inteligência artificial (IA) tem promovido transformações significativas em diversos setores, inclusive na administração pública, ao viabilizar melhorias na prestação de serviços por meio de tecnologias avançadas. O uso crescente da IA, no entanto, exige uma reflexão crítica sobre seus impactos na gestão pública, especialmente à luz dos princípios que regem a atuação do Estado. É necessário considerar tanto os avanços proporcionados por essa tecnologia quanto os desafios que sua implementação pode trazer, com vistas a promover maior agilidade, precisão e economia na administração pública, além de aprimorar a experiência do cidadão no acesso aos serviços oferecidos. Considerando que o fragmento de texto acima tem caráter unicamente motivador, redija um texto dissertativo a respeito do uso da IA no contexto da administração pública. Em seu texto, aborde os seguintes aspectos: 1 dois benefícios e duas limitações relacionados à infraestrutura tecnológica ou à integração de sistemas para o uso da IA na administração pública; [valor: 7,00 pontos] 2 dois exemplos práticos e tecnicamente viáveis de aplicação da IA em sistemas públicos de grande escala, bem como a abordagem técnica adequada para cada um deles. [valor: 7,25 pontos]
        """,
        required=("dois benefícios de infraestrutura/integração para IA", "duas limitações de infraestrutura/integração para IA", "dois exemplos de IA em sistemas públicos de grande escala e abordagem técnica de cada um"),
        theme="Inteligência artificial na administração pública", subthemes=("infraestrutura de IA", "integração de sistemas", "computação em nuvem", "APIs e microsserviços", "NLP", "aprendizado de máquina", "LLMs", "visão computacional"),
        situation="Avaliação de benefícios, limitações e aplicações tecnicamente viáveis de IA em sistemas públicos de grande escala.", citations=("IA", "cloud", "data lake/lakehouse", "APIs", "microsserviços", "deep learning", "LLM", "NLP", "RAG"),
        scope="específico", match="direta",
        mapped_items=("INTELIGÊNCIA ARTIFICIAL — 1 Inteligência artificial: fundamentos e aplicações.", "INTELIGÊNCIA ARTIFICIAL — 2 Aprendizado de máquina.", "INTELIGÊNCIA ARTIFICIAL — 4 Redes Neurais e Deep Learning. Arquiteturas de redes neurais, Frameworks, técnicas de treinamento e aplicações.", "INTELIGÊNCIA ARTIFICIAL — 5 Processamento de linguagem natural. Modelos, pré‐processamento, agentes inteligentes e sistemas multiagentes.", "INTELIGÊNCIA ARTIFICIAL — 6 Arquitetura e engenharia de sistemas de IA. MLOps. Deploy de modelos. Integração com computação em nuvem.", "ARQUITETURA DE SOFTWARE — 3 Sistemas de N camadas; microsserviço.", "ARQUITETURA DE SOFTWARE — 5 APIs, arquitetura cloud native.", "ARQUITETURA DE SOFTWARE — 8 Barramento de serviços corporativos (ESB); interoperabilidade entre aplicações."),
        pattern=ms_patterns[0], proof_url=URLS["ms_prova"], answer_url=URLS["ms_padrao"], source_statement="caderno oficial, PDF p. 1", source_answer="padrão definitivo, PDF pp. 1–2",
    ))
    rows.append(base_question(
        qid="tce_ms_2025_ace_ti_q2", contest=ms, kind="questão dissertativa", lines=20, points=15,
        statement="""
        No que concerne à contratação de bens e serviços de TI pela administração pública, redija um texto dissertativo abordando os seguintes aspectos: 1 os deveres do fiscal na fiscalização da execução do contrato, conforme as previsões da Lei n.º 14.133/2021. [valor: 5,25 pontos] 2 as fases do processo de contratação de TI, bem como pelo menos dois aspectos relevantes de cada fase, de acordo com a IN SGD/ME n.º 94/2022. [valor: 9,00 pontos]
        """,
        required=("deveres do fiscal do contrato", "fases do processo de contratação de TI", "dois aspectos relevantes de cada fase"),
        theme="Contratação e fiscalização de bens e serviços de TI", subthemes=("fiscalização contratual", "planejamento", "seleção do fornecedor", "gestão do contrato", "DFD", "ETP", "TR", "gerenciamento de riscos"),
        situation="Exposição normativa sobre fiscalização e fases da contratação pública de TI.", citations=("Lei n.º 14.133/2021", "IN SGD/ME n.º 94/2022"), scope="específico", match="direta",
        mapped_items=("GESTÃO E GOVERNANÇA DE TI — 6 Contratações de TI no setor público.", "CONTRATAÇÕES DE TI — 1 Gestão de contratação de soluções de TI.", "CONTRATAÇÕES DE TI — 2 Legislação aplicável à contratação de bens e serviços de TI e suas alterações.", "CONTRATAÇÕES DE TI — 2.1 Lei nº 14.133/2021.", "CONTRATAÇÕES DE TI — 2.2 Instrução Normativa SGD/ME nº 94/2022."),
        pattern=ms_patterns[1], proof_url=URLS["ms_prova"], answer_url=URLS["ms_padrao"], source_statement="caderno oficial, PDF p. 2", source_answer="padrão definitivo, PDF pp. 3–4",
        notes="O cabeçalho desta questão no padrão definitivo registra 25/10/2025; o caderno e o restante da prova registram 26/10/2025.",
    ))
    rows.append(base_question(
        qid="tce_ms_2025_ace_ti_q3", contest=ms, kind="questão dissertativa", lines=20, points=15,
        statement="""
        Uma empresa de comércio eletrônico identificou que, durante os finais de semana, o tempo de resposta do seu site aumenta de forma expressiva, o que gera reclamações de clientes e abertura de diversos chamados no service desk. Além disso, o contrato firmado entre a empresa e seus clientes prevê que o site deve manter 95% de disponibilidade mensal, mas o relatório do último mês evidenciou apenas 91%. Durante análise, verificou-se que não havia informações completas sobre dependências entre serviços e infraestrutura, dificultando a identificação da causa-raiz do problema. A partir da situação hipotética apresentada, redija, com base no ITIL V4, um texto dissertativo a respeito de gestão e segurança de tecnologia da informação. Em seu texto, atenda ao que se pede a seguir. 1 Explique o papel do gerenciamento de problemas e como ele deve atuar para evitar que se repitam as falhas de desempenho do site aos finais de semana. [valor: 5,00 pontos] 2 Discorra sobre o papel do gerenciamento de nível de serviço diante da quebra do acordo de disponibilidade com os clientes. [valor: 5,00 pontos] 3 Explique de que forma o gerenciamento de configuração de serviço poderia ter contribuído para reduzir o impacto e acelerar a solução dos problemas da empresa em apreço. [valor: 4,25 pontos]
        """,
        required=("papel do gerenciamento de problemas e prevenção de recorrência", "gerenciamento de nível de serviço diante do SLA descumprido", "gerenciamento de configuração para reduzir impacto e acelerar solução"),
        theme="Gestão de serviços de TI (ITIL v4)", subthemes=("gerenciamento de problemas", "nível de serviço", "SLA", "disponibilidade", "gerenciamento de configuração", "CMDB", "causa-raiz"),
        situation="Site com degradação recorrente, SLA de disponibilidade descumprido e dados incompletos de dependências.", citations=("ITIL v4", "SLA", "service desk", "CMDB"), scope="específico", match="direta",
        mapped_items=("GESTÃO E GOVERNANÇA DE TI — 3 Gestão de serviços de TI (ITIL v4).",), pattern=ms_patterns[2],
        proof_url=URLS["ms_prova"], answer_url=URLS["ms_padrao"], source_statement="caderno oficial, PDF p. 3", source_answer="padrão definitivo, PDF p. 5",
    ))
    rows.append(base_question(
        qid="tce_ms_2025_ace_ti_peca", contest=ms, kind="peça de natureza técnica — parecer", lines=60, points=55,
        statement="""
        Um órgão da administração pública federal realizou a contratação direta, por inexigibilidade, de uma empresa para desenvolvimento e implantação de um novo sistema de processo eletrônico. O processo foi instruído com estudo técnico preliminar (ETP) genérico, que não detalhava os requisitos da solução nem apresentava um levantamento aprofundado de alternativas no mercado, encerrando-se com uma alegação sucinta de inviabilidade de competição para justificar a inexigibilidade. Na fase de seleção, a análise da proposta técnica da empresa contratada consistiu simplesmente na expressão “De acordo”, dada por um gestor, sem parecer técnico que avaliasse o alinhamento da solução ofertada com os requisitos do órgão. Após seis meses de execução contratual, período no qual os pagamentos estavam sendo realizados com base nas horas trabalhadas pela equipe da contratada (pagamento por esforço), o órgão celebrou um termo aditivo que aumentou o valor global do contrato em 35%, sob a mera justificativa de “novas necessidades funcionais”. A partir da situação hipotética apresentada, elabore um parecer técnico acerca da condução do processo de contratação descrito, com fundamentação jurídica e técnica, à luz da legislação vigente e dos princípios da administração pública. Em seu parecer, analise os seguintes aspectos: 1 escolha da contratação direta por inexigibilidade na situação, abordando três pressupostos legais indispensáveis para sua caracterização; [valor: 16,60 pontos] 2 irregularidade do ETP elaborado no caso, considerando sua finalidade, e princípio administrativo violado na situação; [valor: 10,20 pontos] 3 irregularidade da análise da proposta técnica feita na situação, considerando sua finalidade, e exemplos de itens a serem verificados; [valor: 9,60 pontos] 4 modalidade de pagamento adotada e riscos a ela associados, recomendando outra modalidade de pagamento mais apropriada e esclarecendo a necessidade de cláusulas de nível de serviço (SLA); [valor: 11,85 pontos] 5 legalidade do termo aditivo celebrado, indicando o limite percentual admitido pela legislação vigente para acréscimos contratuais. [valor: 4,00 pontos]
        """,
        required=("inexigibilidade e três pressupostos legais", "finalidade e deficiência do ETP e princípio violado", "finalidade e deficiência da análise técnica e itens de verificação", "pagamento por esforço, riscos, alternativa por resultados e SLA", "legalidade do aditivo e limite percentual"),
        theme="Parecer sobre contratação direta e execução de contrato de TI", subthemes=("inexigibilidade", "ETP", "análise de proposta técnica", "requisitos funcionais e não funcionais", "pagamento por esforço", "pontos de função", "SLA", "acréscimo contratual"),
        situation="Contratação direta de sistema com planejamento deficiente, análise técnica insuficiente, pagamento por horas e aditivo de 35%.", citations=("Lei n.º 14.133/2021", "IN SGD/ME n.º 94/2022", "Lei n.º 9.784/1999", "ITIL", "COBIT", "SLA", "pontos de função"), scope="específico", match="direta",
        mapped_items=("ENGENHARIA DE SOFTWARE — 4 Elicitação e gerenciamento de requisitos.", "GESTÃO E GOVERNANÇA DE TI — 1 Governança corporativa de TI (COBIT 2019, ISO/IEC 38500).", "GESTÃO E GOVERNANÇA DE TI — 3 Gestão de serviços de TI (ITIL v4).", "GESTÃO E GOVERNANÇA DE TI — 6 Contratações de TI no setor público.", "CONTRATAÇÕES DE TI — 1 Gestão de contratação de soluções de TI.", "CONTRATAÇÕES DE TI — 2.1 Lei nº 14.133/2021.", "CONTRATAÇÕES DE TI — 2.2 Instrução Normativa SGD/ME nº 94/2022."),
        pattern=ms_patterns[3], proof_url=URLS["ms_prova"], answer_url=URLS["ms_padrao"], source_statement="caderno oficial, PDF p. 4", source_answer="padrão definitivo, PDF pp. 6–7",
    ))
    return rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    contest_fields = [
        "id_concurso", "ano", "orgao", "cargo", "especialidade", "banca", "tipo_orgao", "nivel_cargo",
        "categoria_comparabilidade", "url_edital", "url_prova", "url_padrao_resposta", "fonte_oficial",
        "status_confirmacao", "observacoes",
    ]
    question_fields = [
        "id_questao", "id_concurso", "ano", "orgao", "cargo", "especialidade", "tipo_discursiva",
        "numero_maximo_linhas", "pontuacao", "enunciado_integral", "itens_exigidos", "tema_principal",
        "subtemas", "situacao_problema", "norma_ou_tecnologia_citada", "conhecimento_geral_ou_especifico",
        "correspondencia_com_edital_tce_ma", "itens_correspondentes_tce_ma", "texto_padrao_resposta",
        "url_prova", "url_padrao_resposta", "fonte_enunciado", "fonte_padrao_resposta", "status_confirmacao",
        "observacoes",
    ]
    write_csv(ROOT / "dataset/concursos.csv", contest_fields, CONCURSOS)
    write_csv(ROOT / "dataset/questoes_discursivas.csv", question_fields, build_questions())


if __name__ == "__main__":
    main()
