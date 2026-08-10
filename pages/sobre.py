import dash
from dash import html, dcc, callback, Input, Output

dash.register_page(__name__, path='/sobre')

from data_source import (
    load_sobre,
    load_equipe,
)


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
                        className="page-title",children="Inteligência Territorial para Resiliência e Integração de Indicadores para HIS no Estado de São Paulo"
                    ),
                ],
            ),
    ],
    
    ),
    html.Div(className="row", children=[
        html.Div(className="col-lg-8 col-sm-12", children=[
            html.Div(children=[
                            dcc.Markdown(load_sobre())
                        ]),
        ]),
        html.Div(className="col-lg-4 col-sm-12", children=[
            html.Div(className="card bg-primary text-primary-fg", children=[
                html.Div(className="card-body", children=[
                    html.Div(children=[
                        dcc.Markdown(load_equipe())
                    ])
                ])
            ]),
            
        ]),
        
    ]),
    

       ]