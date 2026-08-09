import dash
import plotly.graph_objects as go
from dash import Input, Output, callback, dcc, html

from data_source import (
    get_simplified_geometry,
    load_df_indicadores,
    load_df_irct_filtrado,
    load_gdf,
)

dash.register_page(__name__, path="/")


layout = [
    # html.H3(children="IRCT", style={"textAlign": "right"}),
    html.Div(
        className="row mb-2 mt-4",
        children=[
            html.Div(
                id="titulo",
                className="col-lg-8 col-sm-12",
                children=[
                    html.Div(className="page-pretitle", children="Home"),
                    html.H1(
                        className="page-title",
                        children="Índice de Resiliência Climática e Territorial",
                    ),
                ],
            ),
            html.Div(
                className="col-lg-4 col-sm-12",
                children=[
                    dcc.Dropdown(
                        options=[
                            "Índice de Resiliência Climática e Territorial",
                            "Mitigação",
                            "Adaptação",
                            "Déficit Habitacional",
                            "Vulnerabilidade Social",
                        ],
                        value="Índice de Resiliência Climática e Territorial",
                        clearable=False,
                        id="dropdown-indice",
                    )
                ],
            ),
        ],
    ),
    html.Div(
        className="row mb-3",
        children=[
            html.Div(
                id="texto-explicativo", className="col-lg-12 col-sm-12", children=[]
            ),
            html.Div(
                className="col-lg-12 col-sm-12",
                children=[
                    html.Div(
                        className="card h-100",
                        children=[
                            dcc.Loading(
                                dcc.Graph(
                                    id="mapa-indice",
                                    config={
                                        "displayModeBar": False,
                                        "scrollZoom": False,
                                    },
                                    style={"width": "100%"},
                                )
                            )
                        ],
                    )
                ],
            ),
        ],
    ),
    html.Div(id="click", children=[dcc.Location(id="url-loc")]),
]


def mapa_indice(indice):
    gdf = load_gdf()
    gdf_filtrado = load_df_irct_filtrado(load_df_indicadores())

    fig = go.Figure()

    fig.add_trace(
        go.Choropleth(
            geojson=get_simplified_geometry(gdf, background=True),
            locations=gdf.index,
            z=[1] * len(gdf),
            colorscale=[[0, "lightgray"], [1, "lightgray"]],
            showscale=False,
            marker_line_color="white",
            marker_line_width=0.5,
            hoverinfo="skip",
        )
    )

    fig.add_trace(
        go.Choropleth(
            geojson=get_simplified_geometry(gdf_filtrado),
            locations=gdf_filtrado.index,
            z=gdf_filtrado[indice],
            colorscale="Viridis",
            marker_line_color="white",
            marker_line_width=0.5,
            colorbar_title="Índice",
            colorbar={"orientation": "h", "y": -0.15},
            text=gdf_filtrado["NM_MUN"],
            hovertemplate=("<b>%{text}</b><br>Índice: %{z:.2f}<extra></extra>"),
        )
    )

    xmin, ymin, xmax, ymax = gdf_filtrado.total_bounds

    dx = (xmax - xmin) * 0.10
    dy = (ymax - ymin) * 0.20

    fig.update_geos(
        visible=False,
        lonaxis_range=[xmin - dx, xmax + dx],
        lataxis_range=[ymin - dy, ymax + dy],
    )

    fig.update_layout(
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        paper_bgcolor="white",
        plot_bgcolor="white",
        height=650,
    )

    return fig


def texto_explicativo(indice):
    texto: dcc.Markdown = dcc.Markdown("")
    if indice == "Índice de Resiliência Climática e Territorial":
        texto = dcc.Markdown(""" 
                O Índice de Resiliência Climática e Territorial (IRCT) é uma ferramenta desenvolvida 
                para qualificar os municípios e avaliar seu nível de adequação em relação à resiliência climática e territorial, 
                considerando sua interação com a vulnerabilidade social e habitacional. 
                O índice é construído por meio de modelagem fuzzy e integra quatro dimensões: **Mitigação** Climática, **Adaptação** Climática, 
                **Déficit Habitacional** e **Vulnerabilidade Social**. Cada uma dessas dimensões é representada por um subíndice, 
                também calculado por meio de modelagem fuzzy, a partir de um conjunto de 44 indicadores que caracterizam diferentes 
                aspectos das condições ambientais, territoriais, habitacionais e sociais dos municípios.
                """)
    elif indice == "Mitigação":
        texto = dcc.Markdown(""" 
                O Subíndice de Mitigação é uma dimensão do IRCT que avalia a capacidade dos municípios de contribuir para a redução 
                dos impactos associados às mudanças climáticas por meio de estratégias e condições relacionadas ao ambiente urbano. 
                Sua construção considera três grupos de fatores: **Redução de Calor**, **Mitigação de Carbono** e **Gestão Ambiental Urbana**, 
                que abrangem diferentes aspectos da estrutura e das condições ambientais dos municípios. 
                O subíndice é calculado por meio de modelagem fuzzy, utilizando **9 dos 44 indicadores** selecionados para a pesquisa, 
                de modo a integrar diferentes variáveis e representar, de forma conjunta, o desempenho municipal em relação à mitigação climática.
                """)
    elif indice == "Adaptação":
        texto = dcc.Markdown(""" 
                O Subíndice de Déficit Habitacional é uma dimensão do IRCT que avalia as condições habitacionais dos municípios, 
                considerando tanto a insuficiência quanto a inadequação das moradias. 
                Sua construção contempla dois grupos de fatores: **Déficit Qualitativo** e **Déficit Quantitativo**, 
                permitindo considerar diferentes aspectos relacionados à necessidade de melhorias nas condições existentes e à 
                demanda por novas unidades habitacionais. 
                O subíndice é calculado por meio de modelagem fuzzy, utilizando **10 dos 44 indicadores** selecionados para a pesquisa, 
                integrando essas variáveis para representar as condições do déficit habitacional nos municípios.
                """)
    elif indice == "Déficit Habitacional":
        texto = dcc.Markdown(""" 
                O Subíndice de Vulnerabilidade Social é uma dimensão do IRCT que avalia condições sociais que podem influenciar a 
                capacidade da população de enfrentar situações de risco e vulnerabilidade no território. 
                Sua construção considera três grupos de fatores: **Necessidade de Serviços de Saúde**, **Acesso à Educação** e **Condições Socioeconômicas**, 
                contemplando aspectos relacionados ao acesso a serviços essenciais e às condições de vida da população. 
                O subíndice é calculado por meio de modelagem fuzzy, utilizando **11 dos 44 indicadores** selecionados para a pesquisa, 
                integrando essas variáveis para representar as diferentes dimensões da vulnerabilidade social nos municípios.
                """)
    return texto


@callback(
    Output("mapa-indice", "figure"),
    Output("titulo", "children"),
    Output("texto-explicativo", "children"),
    Input("dropdown-indice", "value"),
)
def update_graph(value):

    # output do mapa
    mapa = mapa_indice(value)

    # output do título

    titulo = [
        html.Div(className="page-pretitle", children="Home"),
        html.H1(className="page-title", children=value),
    ]

    # output do texto
    texto = texto_explicativo(value)
    return mapa, titulo, texto


@callback(
    Output("url-loc", "href"),
    Input("mapa-indice", "clickData"),
    prevent_initial_call=True,
)
def update_click(clickData):

    return f"./cidades#{clickData['points'][0]['text']}"

