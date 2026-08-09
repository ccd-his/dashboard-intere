from functools import cache

import dash
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
from dash import Input, Output, callback, dcc, html

from data_source import (
    get_simplified_geometry,
    load_clusters,
    load_df_irct_filtrado,
    load_gdf,
)
from ui import make_avatar, make_table

dash.register_page(__name__, path="/agrupamentos")


# Carregar dados
gdf = load_gdf()

df = load_clusters()

cidades = df["Município"].unique()

gdf_filtrado = load_df_irct_filtrado(df)


layout = [
    # html.H3(children="IRCT", style={"textAlign": "right"}),
    html.Div(
        className="row mb-2 mt-4",
        children=[
            html.Div(
                id="titulo-cluster",
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
                        id="dropdown-indice-cluster",
                    )
                ],
            ),
        ],
    ),
    html.Div(
        className="row mb-3",
        children=[
            html.Div(
                id="texto-explicativo-cluster",
                className="col-lg-12 col-sm-12",
                children=[],
            ),
            html.Div(
                className="col-lg-12 col-sm-12",
                children=[
                    html.Div(
                        className="card h-100",
                        children=[
                            dcc.Loading(
                                dcc.Graph(
                                    id="mapa-indice-cluster",
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
    html.Div(className="row mb-3", children=[html.Div(id="caracteristicas-cluster")]),
]


@cache
def mapa_indice_cluster(indice):

    if indice == "Índice de Resiliência Climática e Territorial":
        cores = {"0": "#dada2a", "1": "#35b779", "2": "#31688e", "3": "#440154"}
    elif indice == "Mitigação":
        cores = {"0": "#d8f6ac", "1": "#9ed4a5", "2": "#42a6cc", "3": "#084081"}
    elif indice == "Adaptação":
        cores = {"0": "#cce07c", "1": "#95c368", "2": "#379e54", "3": "#004529"}
    elif indice == "Déficit Habitacional":
        cores = {"0": "#ecdb8f", "1": "#fece65", "2": "#e1640e", "3": "#662506"}
    elif indice == "Vulnerabilidade Social":
        cores = {"0": "#f3bb9f", "1": "#f18496", "2": "#cd238f", "3": "#49006a"}

    dados = gdf_filtrado.copy()

    # Trata os clusters como categorias
    dados["cluster"] = dados[indice].astype(str)

    fig = px.choropleth(
        dados,
        geojson=get_simplified_geometry(dados),
        locations=dados.index,
        color="cluster",
        color_discrete_map=cores,
        category_orders={"cluster": ["0", "1", "2", "3"]},
        hover_name="NM_MUN",
    )

    fig.update_traces(
        hovertemplate=("<b>%{hovertext}</b><br>Cluster: %{customdata}<extra></extra>"),
        customdata=dados[indice],
        marker_line_color="white",
        marker_line_width=0.5,
    )

    fig.update_geos(visible=False, fitbounds="locations")

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="white",
        plot_bgcolor="white",
        height=650,
        legend=dict(
            title="Agrupamento",
            orientation="h",
            yanchor="top",
            y=-0.05,
            xanchor="center",
            x=0.5,
        ),
    )

    return fig


def texto_explicativo_cluster(indice):
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
                O Subíndice de Adaptação Climática é uma dimensão do IRCT que avalia as condições dos municípios para enfrentar 
                e responder aos impactos e riscos associados às mudanças climáticas. 
                Sua construção considera quatro grupos de fatores: **Eventos Extremos**, **Exposição ao Risco**, **Segurança Alimentar** e **Orçamento**, 
                contemplando aspectos relacionados à ocorrência de eventos climáticos, à exposição da população e do território a riscos, 
                à capacidade de garantir condições de segurança alimentar e à disponibilidade de recursos para ações de adaptação. 
                O subíndice é calculado por meio de modelagem fuzzy, utilizando **16 dos 44 indicadores** selecionados para a pesquisa, 
                integrando diferentes variáveis para representar a capacidade municipal de adaptação climática.
                """)
    elif indice == "Déficit Habitacional":
        texto = dcc.Markdown(""" 
                O Subíndice de Déficit Habitacional é uma dimensão do IRCT que avalia as condições habitacionais dos municípios, 
                considerando tanto a insuficiência quanto a inadequação das moradias. 
                Sua construção contempla dois grupos de fatores: **Déficit Qualitativo** e **Déficit Quantitativo**, 
                permitindo considerar diferentes aspectos relacionados à necessidade de melhorias nas condições existentes e à 
                demanda por novas unidades habitacionais. 
                O subíndice é calculado por meio de modelagem fuzzy, utilizando **10 dos 44 indicadores** selecionados para a pesquisa, 
                integrando essas variáveis para representar as condições do déficit habitacional nos municípios.
                """)
    elif indice == "Vulnerabilidade Social":
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
    Output("mapa-indice-cluster", "figure"),
    Output("titulo-cluster", "children"),
    Output("texto-explicativo-cluster", "children"),
    Output("caracteristicas-cluster", "children"),
    Input("dropdown-indice-cluster", "value"),
)
def update_graph_cluster(value):
    df_clusters = pd.read_csv(
        "https://raw.githubusercontent.com/ccd-his/dashboard-intere/refs/heads/main/data/caracteristicas_clusters.csv"
    )
    # output do mapa
    mapa = mapa_indice_cluster(value)

    # output do título

    titulo = [
        html.Div(className="page-pretitle", children="Agrupamentos"),
        html.H1(className="page-title", children=value),
    ]

    # output do texto
    texto = texto_explicativo_cluster(value)

    # caracteristicas dos clusters[]
    df_clusters = df_clusters[df_clusters["Indicador"] == value]

    df_clusters = df_clusters[["Agrupamento", "Características", "Municípios"]]
    caracteristicas = dag.AgGrid(
        id="get-started-example-basic-df",
        rowData=df_clusters.to_dict("records"),
        columnDefs=[
            {"field": i, "cellRenderer": "markdown"} for i in df_clusters.columns
        ],
        style={"width": "100%"},
        columnSize="sizeToFit",
        columnSizeOptions={
            "defaultMinWidth": 100,
            "columnLimits": [{"key": "Indicador", "minWidth": 200}],
        },
    )
    return (
        mapa,
        titulo,
        texto,
        [
            # caracteristicas,
            make_table(
                "Características",
                ["Grupo", "Características", "Municípios"],
                df_clusters.values.tolist(),
                ["w-1 text-center", "w-50", "w-50"],
                ["text-center", "", "text-secondary"],
                [ lambda t: make_avatar(t, "gray-50"),lambda t: texto_markdown(t), None, None]
            ),
        ],
    )

def texto_markdown(txt):
    return dcc.Markdown(txt)