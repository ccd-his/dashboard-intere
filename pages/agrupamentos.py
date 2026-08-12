from functools import lru_cache

import dash
import plotly.express as px
from dash import Input, Output, callback, dcc, html

from data_source import (
    get_simplified_geometry_clusters,
    load_clusters,
    load_df_clusters_filtrado,
    load_df_textos_agrupamentos,
    load_caracteristicas_clusters,
)
from ui import make_avatar, make_table

dash.register_page(__name__, path="/agrupamentos")


@lru_cache(maxsize=1)
def _get_page_data():
    df = load_clusters()
    cidades = df["Município"].unique()
    gdf_filtrado = load_df_clusters_filtrado()
    return df, cidades, gdf_filtrado


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


def mapa_indice_cluster(indice):
    _, _, gdf_filtrado = _get_page_data()

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
        geojson=get_simplified_geometry_clusters(),
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
    textos = load_df_textos_agrupamentos()
    paragrafo = textos[textos["Índice"]==indice]['Texto']

    return dcc.Markdown(paragrafo)


@callback(
    Output("mapa-indice-cluster", "figure"),
    Output("titulo-cluster", "children"),
    Output("texto-explicativo-cluster", "children"),
    Output("caracteristicas-cluster", "children"),
    Input("dropdown-indice-cluster", "value"),
)
def update_graph_cluster(value):
    df_clusters = load_caracteristicas_clusters()
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

    df_clusters = df_clusters[["Agrupamento", "Características"]]

    tabela =make_table(
                "tabela-clusters",
                ["Grupos", "Características e Recomendações"],
                df_clusters.values.tolist(),
                ["w-1 text-center", "w-99"],
                ["text-center", ""],
                [ lambda t: make_avatar(t, "gray-50"),lambda t: texto_markdown(t)]
            ),

    return (
        mapa,
        titulo,
        texto,
        tabela
    )

def texto_markdown(txt):
    return dcc.Markdown(txt)
