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
    #html.H3(children="IRCT", style={"textAlign": "right"}),
    html.Div(className="row mb-2 mt-4", children=[
        html.Div(className="col-10", children=[
            html.Div(className="page-pretitle",children="Home"),
            html.H1(className="page-title",children="Conheça a situação da sua cidade")
        ])
    ]),
    html.Div(className="row mb-2", children=[
        html.Div(className="col-5" ,children=[
            html.Div(className="card  mb-5", children=[
                dcc.Graph(id="mapa-cidade")
            ])
        ]),
        html.Div(className="col-7",children=[
            html.Div(className="row", children=[
                html.Div(className="col-5", children=[
                    html.Div(className="card p-3 h-100", id="card-irct", children=[
                      html.H4(className="card-title mb-1", children="Índice de Resiliência Climática Territorial"),
                      html.Div(className="row g-2 align-items-center", children=[
                          html.Div(className="col-auto mt-5 mb-5", children=[
                              html.H1("5.3", style={"fontSize": "4rem"})
                          ]),
                          html.Div(className="progress progress-sm", children=[
                              html.Div(className="progress-bar", style={"width":"53%"}, role="progressbar")
                          ])
                          
                      ])  
                    ])
                ]),
                html.Div(className="col-7",children=[
                    html.Div(className="row mb-2",children=[
                        html.Div(className="col-6",children=[
                            html.Div(className="card p-2", id="card-mitigacao", children=[
                                html.H4(className="card-title mb-1", children="Mitigação"),
                                html.Div(className="row g-2 align-items-center", children=[
                                    html.Div(className="col-auto", children=[
                                        html.H2("7.4")
                                    ]),
                                    html.Div(className="progress progress-sm", children=[
                                        html.Div(className="progress-bar", style={"width":"74%"}, role="progressbar")
                                    ])
                                    
                                ])  
                            ])
                        ]),
                        html.Div(className="col-6",children=[
                            html.Div(className="card p-2", id="card-adaptacao", children=[
                                html.H4(className="card-title mb-1", children="Adaptação"),
                                html.Div(className="row g-2 align-items-center", children=[
                                    html.Div(className="col-auto", children=[
                                        html.H2("2.8")
                                    ]),
                                    html.Div(className="progress progress-sm", children=[
                                        html.Div(className="progress-bar", style={"width":"28%"}, role="progressbar")
                                    ])
                                    
                                ])  
                            ])
                        ])
                    ]),
                    html.Div(className="row",children=[
                        html.Div(className="col-6",children=[
                            html.Div(className="card p-2", id="card-deficithabitacional", children=[
                                html.H4(className="card-title mb-1", children="Déficit Habitacional"),
                                html.Div(className="row g-2 align-items-center", children=[
                                    html.Div(className="col-auto", children=[
                                        html.H2("4.0")
                                    ]),
                                    html.Div(className="progress progress-sm", children=[
                                        html.Div(className="progress-bar", style={"width":"40%"}, role="progressbar")
                                    ])
                                    
                                ])  
                            ])
                        ]),
                        html.Div(className="col-6",children=[
                            html.Div(className="card p-2", id="card-vulnerabilidadesocial", children=[
                                html.H4(className="card-title mb-1", children="Vulnerabilidade Social"),
                                html.Div(className="row g-2 align-items-center", children=[
                                    html.Div(className="col-auto", children=[
                                        html.H2("8.2")
                                    ]),
                                    html.Div(className="progress progress-sm", children=[
                                        html.Div(className="progress-bar", style={"width":"82%"}, role="progressbar")
                                    ])
                                    
                                ])  
                            ])
                        ])
                    ]),
                ])
            ]),
            html.Div(className="row",children=[
                html.Div(className="col", children=[
                    html.Div(className="card mt-3 p-3 h-100", id='card-tabela-acoes', children=[
                        "Aqui vai uma tabela com as ações indicadas para melhoria"
                    ])
                ])

            ])
        ])
    ]),
    html.Div(className="row g-2 mb-2", children=[
        html.Div(className="col", children=[
            html.Div(className="card mt-4", id='card-tabela-indicadores', children="Indicadores")
        ])
        
    ])
  
]


@callback(Output("graph-content", "figure"), Input("dropdown-selection", "value"))
def update_graph(value):
    dff = df[df.country == value]
    return px.line(dff, x="year", y="pop")