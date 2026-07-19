import dash
from dash import html
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')

df = pd.read_csv(
    "../data/indicadores.csv"
)


layout = [
    html.H3(children="IRCT", style={"textAlign": "right"}),
    html.Div(className="row g-3 mb-2", children=["linha 1"]),
    html.Div(className="row g-3 mb-2", children=["linha 2"])
  
]


@callback(Output("graph-content", "figure"), Input("dropdown-selection", "value"))
def update_graph(value):
    dff = df[df.country == value]
    return px.line(dff, x="year", y="pop")