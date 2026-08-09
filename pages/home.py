import dash
from dash import html
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import geopandas as gpd
import plotly.graph_objects as go
from pathlib import Path
import dash_ag_grid as dag
from functools import cache

dash.register_page(__name__, path='/')


# Carregar dados
gdf = gpd.read_file("./data/SP_Municipios_2025/SP_Municipios_2025.shp")
gdf = gdf.to_crs(4674)
gdf["CD_MUN"] = gdf["CD_MUN"].astype(str)
gdf = gdf.sort_values("NM_MUN").reset_index(drop=True)

gdf["id"] = gdf.index.astype(str)
df = pd.read_csv(
    "https://raw.githubusercontent.com/ccd-his/dashboard-intere/refs/heads/main/data/indicadores.csv"
)

cidades = df['Município'].unique()

df_irct = df[['Código IBGE','Município','Mitigação','Adaptação','Déficit Habitacional','Vulnerabilidade Social','Índice de Resiliência Climática e Territorial']]
df_irct['Código IBGE'] = df_irct['Código IBGE'].astype('str')
gdf = gdf.merge(df_irct, left_on='CD_MUN',right_on='Código IBGE')


layout = [
    # html.H3(children="IRCT", style={"textAlign": "right"}),

    html.Div(
        className="row mb-2 mt-4",children=[
            html.Div(id="titulo",
                className="col-lg-8 col-sm-12",children=[
                    html.Div(
                        className="page-pretitle",children="Home"
                    ),
                    html.H1(
                        className="page-title",children="Índice de Resiliência Climática e Territorial"
                    ),
                ],
            ),

            html.Div(
                className="col-lg-4 col-sm-12",children=[
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
                id="texto-explicativo",
                className="col-lg-12 col-sm-12", children=[
                    
                ]

            ),

            html.Div(
                className="col-lg-12 col-sm-12",children=[
                    html.Div(
                        className="card h-100",children=[
                            dcc.Loading(dcc.Graph(
                                id="mapa-indice",
                                config={"displayModeBar": False, 'scrollZoom': False},
                            ))
                        ],
                    )
                ],
            ),
        ]),
    html.Div(id='click',children=[dcc.Location(id="url-loc")])
]

@cache
def mapa_indice(indice):
    fig = go.Figure(
        go.Choropleth(
            geojson=gdf.__geo_interface__,
            locations=gdf.index,
            z=gdf[indice],
            #featureidkey="id",
            colorscale="Viridis",
            #zmin=0.0,
            #zmax=10,
            marker_line_color="white",
            marker_line_width=0.5,
            colorbar_title="Índice",
            colorbar=dict(orientation='h', y=-0.15 ),
            text=gdf.NM_MUN,
            hovertemplate=(
                "<b>%{text}</b><br>"
                "Índice: %{z:.2f}"
                "<extra></extra>"
            ),
            #text="",
            #autocolorscale=True,
            
        )
    )

    fig.update_geos(
        fitbounds="locations",
        visible=False
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="white",
        plot_bgcolor="white",
        height=650,
    )
    return fig

def texto_explicativo(indice):
    if indice == "Índice de Resiliência Climática e Territorial":
        texto = dcc.Markdown(''' 
                O Índice de Resiliência Climática e Territorial (IRCT) é uma ferramenta desenvolvida 
                para qualificar os municípios e avaliar seu nível de adequação em relação à resiliência climática e territorial, 
                considerando sua interação com a vulnerabilidade social e habitacional. 
                O índice é construído por meio de modelagem fuzzy e integra quatro dimensões: **Mitigação** Climática, **Adaptação** Climática, 
                **Déficit Habitacional** e **Vulnerabilidade Social**. Cada uma dessas dimensões é representada por um subíndice, 
                também calculado por meio de modelagem fuzzy, a partir de um conjunto de 44 indicadores que caracterizam diferentes 
                aspectos das condições ambientais, territoriais, habitacionais e sociais dos municípios.
                ''')
    elif indice == "Mitigação":
        texto = dcc.Markdown(''' 
                O Subíndice de Mitigação é uma dimensão do IRCT que avalia a capacidade dos municípios de contribuir para a redução 
                dos impactos associados às mudanças climáticas por meio de estratégias e condições relacionadas ao ambiente urbano. 
                Sua construção considera três grupos de fatores: **Redução de Calor**, **Mitigação de Carbono** e **Gestão Ambiental Urbana**, 
                que abrangem diferentes aspectos da estrutura e das condições ambientais dos municípios. 
                O subíndice é calculado por meio de modelagem fuzzy, utilizando **9 dos 44 indicadores** selecionados para a pesquisa, 
                de modo a integrar diferentes variáveis e representar, de forma conjunta, o desempenho municipal em relação à mitigação climática.
                ''')
    elif indice == "Adaptação":
        texto = dcc.Markdown(''' 
                O Subíndice de Déficit Habitacional é uma dimensão do IRCT que avalia as condições habitacionais dos municípios, 
                considerando tanto a insuficiência quanto a inadequação das moradias. 
                Sua construção contempla dois grupos de fatores: **Déficit Qualitativo** e **Déficit Quantitativo**, 
                permitindo considerar diferentes aspectos relacionados à necessidade de melhorias nas condições existentes e à 
                demanda por novas unidades habitacionais. 
                O subíndice é calculado por meio de modelagem fuzzy, utilizando **10 dos 44 indicadores** selecionados para a pesquisa, 
                integrando essas variáveis para representar as condições do déficit habitacional nos municípios.
                ''')
    elif indice == "Déficit Habitacional":
        texto = dcc.Markdown(''' 
                O Subíndice de Vulnerabilidade Social é uma dimensão do IRCT que avalia condições sociais que podem influenciar a 
                capacidade da população de enfrentar situações de risco e vulnerabilidade no território. 
                Sua construção considera três grupos de fatores: **Necessidade de Serviços de Saúde**, **Acesso à Educação** e **Condições Socioeconômicas**, 
                contemplando aspectos relacionados ao acesso a serviços essenciais e às condições de vida da população. 
                O subíndice é calculado por meio de modelagem fuzzy, utilizando **11 dos 44 indicadores** selecionados para a pesquisa, 
                integrando essas variáveis para representar as diferentes dimensões da vulnerabilidade social nos municípios.
                ''')
    return texto


@callback(
        Output("mapa-indice", "figure"), 
        Output("titulo",'children'),
        Output("texto-explicativo",'children'),
        Input("dropdown-indice", "value"))
def update_graph(value):

    #output do mapa
    mapa = mapa_indice(value)

    #output do título

    titulo= [
                    html.Div(
                        className="page-pretitle",children="Home"
                    ),
                    html.H1(
                        className="page-title",children=value
                    ),
                ]

    #output do texto
    texto = texto_explicativo(value)
    return mapa, titulo, texto

@callback(
    Output('url-loc','href'),
    Input('mapa-indice','clickData'),
    prevent_initial_call=True
)
def update_click(clickData):
    
    return f"./cidades#{clickData['points'][0]['text']}"