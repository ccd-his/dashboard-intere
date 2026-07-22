import dash
from dash import html, dcc, callback, Input, Output

dash.register_page(__name__, path='/sobre')


layout = [
    # html.H3(children="IRCT", style={"textAlign": "right"}),
    html.Div(
        className="row mb-2 mt-4",children=[
            html.Div(id="titulo",
                className="col-10",children=[
                    html.Div(
                        className="page-pretitle",children="Sobre"
                    ),
                    html.H1(
                        className="page-title",children="Inteligência Territorial para Resiliência"
                    ),
                ],
            ),
    ],
    
    ),
    html.Div(children=[
        dcc.Markdown('''
            O dashboard do projeto **"Inteligência Territorial para a Resiliência: Sistematização e Integração de Indicadores para HIS no Estado de São Paulo"**, desenvolvido no âmbito do **CONTRATO nº 033/2025**, decorrente do Edital de Pesquisa do **CAU SP**, foi concebido para facilitar a consulta, a exploração e a visualização dos indicadores produzidos durante a pesquisa.

            O projeto tem como objetivo apoiar profissionais e gestores públicos — em especial arquitetos, urbanistas e demais agentes envolvidos no planejamento territorial — na formulação e execução de políticas e ações voltadas ao fortalecimento da resiliência climática e territorial, com ênfase na Habitação de Interesse Social (HIS) e nas populações em situação de vulnerabilidade.

            Para isso, foram selecionados indicadores disponíveis para todos os municípios das regiões do ABC Paulista, da Região Metropolitana de Sorocaba (RMS) e da Região Metropolitana de Campinas (RMC). A seleção foi orientada por normas internacionais da série ISO relacionadas ao desenvolvimento urbano sustentável e à resiliência, alinhadas aos Objetivos de Desenvolvimento Sustentável (ODS) da Organização das Nações Unidas (ONU). A partir desses indicadores, foram elaborados subíndices e índices sintéticos por meio de um sistema de inferência fuzzy, permitindo integrar múltiplas dimensões da resiliência de forma transparente e compatível com a natureza complexa dos fenômenos analisados.

            A plataforma reúne mapas, gráficos e tabelas interativas que permitem explorar os resultados, comparar municípios e analisar diferentes dimensões da resiliência territorial. Ao ampliar o acesso aos dados e facilitar sua interpretação, o dashboard busca contribuir para a transparência da pesquisa e apoiar a tomada de decisão por pesquisadores, gestores públicos e demais interessados.   
        ''')
    ])
       ]