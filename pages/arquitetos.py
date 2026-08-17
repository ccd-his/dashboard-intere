import plotly.express as px
from functools import cache

import dash

from dash import Input, Output, callback, ctx, dcc, html
import dash_bootstrap_components as dbc
from pandas import DataFrame

from data_source import (
    load_df_arquitetos,
    load_df_cidades,
)
from ui import make_table, make_title

dash.register_page(__name__, path="/arquitetos")

layout = [
    # html.H3(children="IRCT", style={"textAlign": "right"}),
    dcc.Location(id="url", refresh=True),
    make_title(
        "Conheça a cidade no que diz respeito aos dados do CAU",
        "Arquitetos",
        dcc.Dropdown(load_df_cidades(), "", clearable=False, id="dropdown-cidade"),
    ),
    html.Div(
    className="row g-3 mb-3",
    children=[
        # IRCT
        html.Div(
            className="col-md-3 col-sm-6",
            children=[
                html.Div(
                    className="card p-3 h-100",
                    id="card-profissionais",
                    children=[
                        html.Div(
                            "Profissionais em 2025",
                            className="text-muted small"
                        ),
                        html.H1(
                            id="valor-profissionais",
                            children="9.9",
                            className="mb-0",
                            style={"fontSize": "3rem"}
                        ),
                    ],
                )
            ],
        ),

        # Mitigação
        html.Div(
            className="col-md-3 col-sm-6",
            children=[
                html.Div(
                    className="card p-3 h-100",
                    id="card-empresas",
                    children=[
                        html.Div(
                            "Empresas em 2025",
                            className="text-muted small"
                        ),
                        html.H1(
                            id="valor-empresas",
                            children="9.9",
                            className="mb-0",
                            style={"fontSize": "3rem"}
                        ),
                    ],
                )
            ],
        ),

        # Adaptação
        html.Div(
            className="col-md-3 col-sm-6",
            children=[
                html.Div(
                    className="card p-3 h-100",
                    id="card-rrtssociais",
                    children=[
                        html.Div(
                            "RRTs Sociais em 2025",
                            className="text-muted small"
                        ),
                        html.H1(
                            id="valor-rrtssociais",
                            children="9.9",
                            className="mb-0",
                            style={"fontSize": "3rem"}
                        ),
                    ],
                )
            ],
        ),

        # Déficit Habitacional
        html.Div(
            className="col-md-3 col-sm-6",
            children=[
                html.Div(
                    className="card p-3 h-100",
                    id="card-rrtsselecionados",
                    children=[
                        html.Div(
                            "RRTs Selecionados",
                            className="text-muted small"
                        ),
                        html.H1(
                            id="valor-rrtsselecionados",
                            children="9.9",
                            className="mb-0",
                            style={"fontSize": "3rem"}
                        ),
                    ],
                )
            ],
        ),
    ],
),

html.Div(
    className="row g-3 mb-3",
    children=[
        html.Div(
            className="col-md-6",
            children=[
                html.Div(
                    className="card h-100 p-2",
                    children=[
                        dcc.Loading(
                            dcc.Graph(
                                id="grafico-profissionais",
                                config={"displayModeBar": False}
                            )
                        )
                    ]
                )
            ]
        ),

        html.Div(
            className="col-md-6",
            children=[
                html.Div(
                    className="card h-100 p-2",
                    children=[
                        dcc.Loading(
                            dcc.Graph(
                                id="grafico-empresas",
                                config={"displayModeBar": False}
                            )
                        )
                    ]
                )
            ]
        ),
    ]
),


html.Div(
    className="row g-3 mb-3",
    children=[
        html.Div(
            className="col-md-6",
            children=[
                html.Div(
                    className="card h-100 p-2",
                    children=[
                        dcc.Loading(
                            dcc.Graph(
                                id="grafico-rrtssociais",
                                config={"displayModeBar": False}
                            )
                        )
                    ]
                )
            ]
        ),

        html.Div(
            className="col-md-6",
            children=[
                html.Div(
                    className="card h-100 p-2",
                    children=[
                        dcc.Loading(
                            dcc.Graph(
                                id="grafico-rrtsselecionados",
                                config={"displayModeBar": False}
                            )
                        )
                    ]
                )
            ]
        ),
    ]
),


]


def card_progress_pequeno(indice, valor):


    explicacoes = {
        "Profissionais": "Número de profissionais ativos em 2025",
        "Empresas": "Número de empresas ativas em 2025",
        "RRTs Sociais": "RRTs Sociais em 2025",
        "RRTs Selecionados": "RRTs Selecionados em 2025",
    }

    ids = {
        "Profissionais": "card-profissionais",
        "Empresas": "card-empresas",
        "RRTs Sociais": "card-rrtssociais",
        "RRTs Selecionados": "card-rrtsselecionados",
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
            ],
        ),
    ]
    return card_children


def grafico_linhas(
    df,
    x,
    y,
    serie=None,
    titulo=None,
    nome_x=None,
    nome_y=None
):


    if serie is not None:

        fig = px.line(
            df,
            x=x,
            y=y,
            color=serie,
            markers=True,
            title=titulo,
            labels={
                x: nome_x if nome_x else x,
                y: nome_y if nome_y else y,
                serie: serie
            }
        )

    else:

        fig = px.line(
            df,
            x=x,
            y=y,
            markers=True,
            title=titulo,
            labels={
                x: nome_x if nome_x else x,
                y: nome_y if nome_y else y
            }
        )

    fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        hovermode="x unified"
    )

    return fig


@callback(
    Output("grafico-profisssionais","figure"),
    Output("grafico-empresas","figure"),
    Output("grafico-rrtssociais","figure"),
    Output("grafico-rrtsselecionados","figure"),
    Input("dropdown-cidade","value")
)
def plota_graficos(cidade):
    dados = load_df_arquitetos()
    dados = dados[dados['Município']==cidade]

    df = dados[dados['Tipo']=='Profissional']
    profissionais  = grafico_linhas(df,'variable','value',title='Profissionais Ativos',nome_x="Ano",nome_y="")

    return profissionais, profissionais, profissionais, profissionais



