import urllib.parse
from functools import cache

import dash
import dash_ag_grid as dag
import plotly.graph_objects as go
from dash import Input, Output, callback, ctx, dcc, html
import dash_bootstrap_components as dbc
from pandas import DataFrame

from data_source import (
    load_df_cidades,
    load_df_indicadores,
    load_df_recomendacoes,
    load_df_unidades,
    load_gdf,
    load_df_irct_filtrado,
)
from ui import make_table, make_title

dash.register_page(__name__, path="/cidades")

layout = [
    # html.H3(children="IRCT", style={"textAlign": "right"}),
    dcc.Location(id="url", refresh=True),
    make_title(
        "Conheça a situação da sua cidade",
        "Cidades",
        dcc.Dropdown(load_df_cidades(), "", clearable=False, id="dropdown-cidade"),
    ),
    html.Div(
        className="row mb-3",
        children=[
            html.Div(
                className="col-md-5 col-sm-12",
                children=[
                    html.Div(
                        className="card  h-100",
                        children=[
                            dcc.Loading(
                                dcc.Graph(
                                    id="mapa-cidade",
                                    config={
                                        "displayModeBar": False,
                                        "scrollZoom": False,
                                    },
                                )
                            )
                        ],
                    )
                ],
            ),
            html.Div(
                className="col-md-7 col-sm-12",
                children=[
                    html.Div(
                        className="row",
                        children=[
                            html.Div(
                                className="col-md-5 col-sm-12 mb-3",
                                children=[
                                    html.Div(
                                        className="card p-3 h-100 card card-active",
                                        id="card-irct",
                                        children=[
                                            html.H4(
                                                className="card-title mb-1",
                                                children="Índice de Resiliência Climática Territorial",
                                            ),
                                            html.Div(
                                                className="g-2 align-items-center",
                                                children=[
                                                    html.Div(
                                                        className="col-auto mt-5 mb-5",
                                                        children=[
                                                            html.H1(
                                                                "9.9",
                                                                style={
                                                                    "fontSize": "4rem"
                                                                },
                                                            )
                                                        ],
                                                    ),
                                                    html.Div(
                                                        className="progress progress-sm",
                                                        children=[
                                                            html.Div(
                                                                className="progress-bar",
                                                                style={"width": "99%"},
                                                                role="progressbar",
                                                            )
                                                        ],
                                                    ),
                                                ],
                                            ),
                                        ],
                                    )
                                ],
                            ),
                            html.Div(
                                className="col-md-7 col-sm-12",
                                children=[
                                    html.Div(
                                        className="row mb-2",
                                        children=[
                                            html.Div(
                                                className="col-6",
                                                children=[
                                                    html.Div(
                                                        className="card p-2",
                                                        id="card-mitigacao",
                                                        children=[
                                                            html.H4(
                                                                className="card-title mb-1",
                                                                children="Mitigação",
                                                            ),
                                                            html.Div(
                                                                className="g-2 align-items-center",
                                                                children=[
                                                                    html.Div(
                                                                        className="col-auto",
                                                                        children=[
                                                                            html.H2(
                                                                                "9.9"
                                                                            )
                                                                        ],
                                                                    ),
                                                                    html.Div(
                                                                        className="progress progress-sm",
                                                                        children=[
                                                                            html.Div(
                                                                                className="progress-bar",
                                                                                style={
                                                                                    "width": "99%"
                                                                                },
                                                                                role="progressbar",
                                                                            )
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    )
                                                ],
                                            ),
                                            html.Div(
                                                className="col-6",
                                                children=[
                                                    html.Div(
                                                        className="card p-2",
                                                        id="card-adaptacao",
                                                        children=[
                                                            html.H4(
                                                                className="card-title mb-1",
                                                                children="Adaptação",
                                                            ),
                                                            html.Div(
                                                                className="g-2 align-items-center",
                                                                children=[
                                                                    html.Div(
                                                                        className="col-auto",
                                                                        children=[
                                                                            html.H2(
                                                                                "9.9"
                                                                            )
                                                                        ],
                                                                    ),
                                                                    html.Div(
                                                                        className="progress progress-sm",
                                                                        children=[
                                                                            html.Div(
                                                                                className="progress-bar",
                                                                                style={
                                                                                    "width": "99%"
                                                                                },
                                                                                role="progressbar",
                                                                            )
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    )
                                                ],
                                            ),
                                        ],
                                    ),
                                    html.Div(
                                        className="row",
                                        children=[
                                            html.Div(
                                                className="col-6",
                                                children=[
                                                    html.Div(
                                                        className="card p-2",
                                                        id="card-deficithabitacional",
                                                        children=[
                                                            html.H4(
                                                                className="card-title mb-1",
                                                                children="Déficit Habitacional",
                                                            ),
                                                            html.Div(
                                                                className="g-2 align-items-center",
                                                                children=[
                                                                    html.Div(
                                                                        className="col-auto",
                                                                        children=[
                                                                            html.H2(
                                                                                "9.9"
                                                                            )
                                                                        ],
                                                                    ),
                                                                    html.Div(
                                                                        className="progress progress-sm",
                                                                        children=[
                                                                            html.Div(
                                                                                className="progress-bar",
                                                                                style={
                                                                                    "width": "99%"
                                                                                },
                                                                                role="progressbar",
                                                                            )
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    )
                                                ],
                                            ),
                                            html.Div(
                                                className="col-6",
                                                children=[
                                                    html.Div(
                                                        className="card p-2",
                                                        id="card-vulnerabilidadesocial",
                                                        children=[
                                                            html.H4(
                                                                className="card-title mb-1",
                                                                children="Vulnerabilidade Social",
                                                            ),
                                                            html.Div(
                                                                className="g-2 align-items-center",
                                                                children=[
                                                                    html.Div(
                                                                        className="col-auto",
                                                                        children=[
                                                                            html.H2(
                                                                                "8.2"
                                                                            )
                                                                        ],
                                                                    ),
                                                                    html.Div(
                                                                        className="progress progress-sm",
                                                                        children=[
                                                                            html.Div(
                                                                                className="progress-bar",
                                                                                style={
                                                                                    "width": "82%"
                                                                                },
                                                                                role="progressbar",
                                                                            )
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    )
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className="row",
                        children=[
                            html.Div(
                                className="col",
                                children=[
                                    dcc.Loading(
                                        html.Div(
                                            className="mt-3",
                                            id="card-tabela-acoes",
                                            children=["Recomendações de Melhorias"],
                                        )
                                    ),
                                    html.Div(children=[]),
                                ],
                            )
                        ],
                    ),
                ],
            ),
        ],
    ),
    html.Div(
        className="row g-2 mb-2",
        children=[
            html.Div(
                className="col",
                children=[
                    dcc.Loading(
                        html.Div(
                            className="card overflow-x-auto",
                            id="card-tabela-indicadores",
                            children="Indicadores",
                        )
                    )
                ],
            )
        ],
    ),
]


def card_progress_pequeno(indice, valor):


    explicacoes = {
        "Mitigação": "Valores maiores indicam maior mitigação de emissão de gases de efeito estufa.",
        "Adaptação": "Valores maiores indicam melhor adptação às mudanças climáticas.",
        "Déficit Habitacional": "Valores maiores indicam piores condições habitacionais.",
        "Vulnerabilidade Social": "Valores maiores indicam maiores vulnerabilidades.",
    }

    ids = {
        "Mitigação": "card-mitigacao",
        "Adaptação": "card-adaptacao",
        "Déficit Habitacional": "card-deficithabitacional",
        "Vulnerabilidade Social": "card-vulnerabilidadesocial",
    }

    info_id = ids[indice]

    card_children = [
        html.Div(
            style={
                "position": "relative",
                "width": "100%",
            },
            children=[
                html.H4(
                    className="card-title mb-1",
                    children=indice,
                ),
                html.Button(
                    "ⓘ",
                    id=f"info-{indice}",
                    className="btn btn-link p-0",
                    style={
                        "position": "absolute",
                        "top": "1",
                        "right": "0",
                        "fontSize": "1rem",
                        "color": "#6c757d",
                        "textDecoration": "none",
                        "lineHeight": "1",
                    },
                ),

                dbc.Popover(
                    dbc.PopoverBody(
                        explicacoes[indice]
                    ),
                    target=f"info-{indice}",
                    placement="bottom",
                    trigger="click",
                ),

            ],
        ),

        html.Div(
            className="g-2 align-items-center",
            children=[
                html.Div(
                    className="col-auto",
                    children=[
                        html.H2(valor)
                    ],
                ),


                html.Div(
                    className="progress progress-sm",
                    children=[
                        html.Div(
                            className="progress-bar",
                            style={"width": f"{valor * 10}%"},
                            role="progressbar",
                        )
                    ],
                ),
            ],
        ),
    ]
    return card_children


def card_progress_irct(valor):
    card_children = [
        html.Div(
            className="d-flex justify-content-between align-items-start",
            children=[
                html.H4(
                    className="card-title mb-1",
                    children="Índice de Resiliência Climática Territorial",
                ),

                html.Button(
                    "ⓘ",
                    id="info-irct",
                    className="btn btn-link p-0",
                    style={
                        "fontSize": "1.1rem",
                        "color": "#6c757d",
                        "textDecoration": "none",
                        "lineHeight": "1",
                    },
                ),
            ],
        ),

        dbc.Popover(
            dbc.PopoverBody(
                "IRCT — valores maiores indicam maior resiliência."
            ),
            target="info-irct",
            placement="bottom",
            trigger="click",
        ),

        html.Div(
            className="g-2 align-items-center",
            children=[
                html.Div(
                    className="col-auto mt-5 mb-5",
                    children=[
                        html.H1(
                            valor,
                            style={"fontSize": "4rem"}
                        )
                    ],
                ),

                html.Div(
                    className="progress progress-sm",
                    children=[
                        html.Div(
                            className="progress-bar",
                            style={"width": f"{valor * 10}%"},
                            role="progressbar",
                        )
                    ],
                ),
            ],
        ),
    ]
    return card_children


@cache
def mapa_cidade(nome_municipio):
    #gdf = load_gdf()
    gdf = load_df_irct_filtrado(load_df_indicadores())
    z_min = gdf['Índice de Resiliência Climática e Territorial'].min()
    z_max = gdf["Índice de Resiliência Climática e Territorial"].max()
    if nome_municipio=="Santa Bárbara D'Oeste":
        sel=gdf[gdf["NM_MUN"] == "Santa Bárbara d'Oeste"]
    else:
        sel =   gdf[gdf["NM_MUN"] == nome_municipio]
    #indicadores = load_df_indicadores()
    #indicadores = indicadores[indicadores['Município']==nome_municipio]
    #print(indicadores)
    print(sel)
    fig = go.Figure()

    fig.add_trace(
        go.Choropleth(
            geojson=sel.__geo_interface__,
            locations=sel.index,
            #z=[1],
            z=sel['Índice de Resiliência Climática e Territorial'],
            zmin=z_min,
            zmax=z_max,
            featureidkey="id",
            colorscale="viridis_r",#[[0, "#4C78A8"], [1, "#4C78A8"]],
            showscale=False,
            marker_line_color="black",
            marker_line_width=2,
            text=nome_municipio,
        )
    )

    fig.update_geos(fitbounds="locations", visible=False)

    fig.update_layout(
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        paper_bgcolor="white",
        plot_bgcolor="white",
        modebar_remove=["zoom", "pan", "lasso", "select", "toImage"],
    )
    return fig


@callback(
    Output("mapa-cidade", "figure"),
    Output("card-irct", "children"),
    Output("card-mitigacao", "children"),
    Output("card-adaptacao", "children"),
    Output("card-deficithabitacional", "children"),
    Output("card-vulnerabilidadesocial", "children"),
    Output("card-tabela-acoes", "children"),
    Output("card-tabela-indicadores", "children"),
    Output("url", "hash"),
    Input("dropdown-cidade", "value"),
)
def update_graph(value):
    df = load_df_indicadores()
    df_recomendacoes = load_df_recomendacoes()
    df_unidades = load_df_unidades()
    print(ctx.triggered_id)

    valor = value
    print(valor)
    dff: DataFrame = df[df["Município"] == valor]
    

    # valores para os cards
    irct = round(dff["Índice de Resiliência Climática e Territorial"].values[0], 1)
    mitigacao = round(dff["Mitigação"].values[0], 1)
    adaptacao = round(dff["Adaptação"].values[0], 1)
    deficit = round(dff["Déficit Habitacional"].values[0], 1)
    vulnerabilidade = round(dff["Vulnerabilidade Social"].values[0], 1)

    # outputs dos cards
    irct = card_progress_irct(irct)
    mitigacao = card_progress_pequeno("Mitigação", mitigacao)
    adaptacao = card_progress_pequeno("Adaptação", adaptacao)
    deficit = card_progress_pequeno("Déficit Habitacional", deficit)
    vulnerabilidade = card_progress_pequeno("Vulnerabilidade Social", vulnerabilidade)

    # output do mapa
    mapa = mapa_cidade(valor)

    # output das ações
    tabela_acoes = df_recomendacoes[df_recomendacoes["Município"] == valor][
        ["Sugestões e Recomendações para Melhorias"]
    ]
    acoes = dag.AgGrid(
        id="get-started-example-basic-df",
        rowData=tabela_acoes.to_dict("records"),
        columnDefs=[{"field": i} for i in tabela_acoes.columns],
        style={"height": "250px"},
        columnSize="sizeToFit",
        columnSizeOptions={
            "defaultMinWidth": 100,
            "columnLimits": [{"key": "Indicador", "minWidth": 200}],
        },
    )
    acoes = make_table(
        "sugestoes",
        ["Sugestões e recomendações para melhorias"],
        tabela_acoes.values.tolist(),
        [""],
        [""],
        [lambda t: dcc.Markdown(t)]
    )

    # output dos indicadores
    dff = dff.drop(columns=["Região", "Código IBGE"])
    dados_indicadores = dff.melt(id_vars="Município")
    dados_indicadores.columns = ["Município", "Indicador", "Valor"]
    dados_indicadores = dados_indicadores.merge(
        df_unidades, left_on="Indicador", right_on="Indicador"
    )
    dados_indicadores = dados_indicadores[
        ["Indicador", "Unidade", "Valor", "Período do dado", "Fonte"]
    ]

    indicadores = dag.AgGrid(
        id="get-started-example-basic-df",
        rowData=dados_indicadores.to_dict("records"),
        columnDefs=[{"field": i} for i in dados_indicadores.columns],
        style={"width": "100%"},
        columnSize="sizeToFit",
        columnSizeOptions={
            "defaultMinWidth": 100,
            "columnLimits": [{"key": "Indicador", "minWidth": 200}],
        },
    )

    indicadores2 = make_table(
        "indicadores",
        ["Indicador", "Unidade", "Valor", "Período", "Fonte"],
        dados_indicadores.values.tolist(),
        [
            "w-75",
            "w-1",
            "text-end w-2",
            "text-center w-1",
            "text-center w-25",
        ],
        [
            "",
            "text-secondary",
            "text-end fw-bold",
            "text-secondary text-center",
            "text-center text-secondary",
        ],
    )

    return (
        mapa,
        irct,
        mitigacao,
        adaptacao,
        deficit,
        vulnerabilidade,
        acoes,
        indicadores2,
        "#" + valor,
    )


@callback(
    Output("dropdown-cidade", "value"),
    Input("url", "hash"),
)
def refresh_hash(hash):
    if len(hash) == 0:
        valor = "Sorocaba"
    else:
        valor = hash[1:]
        valor = urllib.parse.unquote(valor)
        if valor == "Santa Bárbara d'Oeste": valor="Santa Bárbara D'Oeste"
    return valor
