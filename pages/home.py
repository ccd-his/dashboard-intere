import dash
from dash import html
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')

df = pd.read_csv(
    "https://raw.githubusercontent.com/ccd-his/dashboard-intere/refs/heads/main/data/indicadores.csv"
)


layout = [
    html.H3(children="IRCT", style={"textAlign": "right"}),
    html.Div(className="row mb-2", children=[
        html.Div(className="col-5",children=[
            html.Div(className="card mt-4 mb-5", children="mapa")
        ]),
        html.Div(className="col-7",children=[
            html.Div(className="row", children=[
                html.Div(className="col-5", children=[
                    html.Div(className="card", children="Índice de Resiliência Climática e Territorial")
                ]),
                html.Div(className="col-7",children=[
                    html.Div(className="row mb-2",children=[
                        html.Div(className="col-6",children=[
                            html.Div(className="card", children="Mitigação")
                        ]),
                        html.Div(className="col-6",children=[
                            html.Div(className="card", children="Adaptação")
                        ])
                    ]),
                    html.Div(className="row mb-2",children=[
                        html.Div(className="col-6",children=[
                            html.Div(className="card", children="Déficit Habitacional")
                        ]),
                        html.Div(className="col-6",children=[
                            html.Div(className="card", children="Vulnerabilidade Social")
                        ])
                    ]),
                ])
            ])
            
        ])
    ]),
    html.Div(className="row g-3 mb-2", children=[
        html.Div(className="card mt-4",children="Indicadores")
    ])
  
]


@callback(Output("graph-content", "figure"), Input("dropdown-selection", "value"))
def update_graph(value):
    dff = df[df.country == value]
    return px.line(dff, x="year", y="pop")