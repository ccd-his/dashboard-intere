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
df_teste = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/wind_dataset.csv")

cidades = df['Município'].unique()

recomendacoes = pd.read_csv('https://raw.githubusercontent.com/ccd-his/dashboard-intere/refs/heads/main/data/recomendacoes.csv')

layout = [
    #html.H3(children="IRCT", style={"textAlign": "right"}),
    html.Div(className="row mb-2 mt-4", children=[
        html.Div(className="col-10", children=[
            html.Div(className="page-pretitle",children="Home"),
            html.H1(className="page-title",children="Conheça a situação da sua cidade")
        ]),
        html.Div(className="col-2", children=[
            dcc.Dropdown(cidades,'Sorocaba',clearable=False,id="dropdown-cidade")
        ])
    ]),
    html.Div(className="row mb-3", children=[
        html.Div(className="col-5" ,children=[
            html.Div(className="card  h-100", children=[
                dcc.Graph(id="mapa-cidade",config={"displayModeBar": False})
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
                    html.Div(className="card mt-3 overflow-x-auto", id='card-tabela-acoes', children=[
                        "Recomendações de Melhorias"
                    ]),
                    html.Div(children=[])
                ])

            ])
        ])
    ]),
    html.Div(className="row g-2 mb-2", children=[
        html.Div(className="col", children=[
            html.Div(className="card overflow-x-auto", id='card-tabela-indicadores', children="Indicadores")
        ])
        
    ])
  
]

def card_progress_pequeno(indice, valor):
    card_children = [html.H4(className="card-title mb-1", children=indice),
                     html.Div(className="row g-2 align-items-center", children=[
                        html.Div(className="col-auto", children=[
                            html.H2(valor)
                        ]),
                        html.Div(className="progress progress-sm", children=[
                            html.Div(className="progress-bar", style={"width":f"{valor*10}%"}, role="progressbar")
                        ])
                                    
                     ]) ] 
    return card_children

def card_progress_irct(valor):
    card_children = [html.H4(className="card-title mb-1", children="Índice de Resiliência Climática Territorial"),
                      html.Div(className="row g-2 align-items-center", children=[
                          html.Div(className="col-auto mt-5 mb-5", children=[
                              html.H1(valor, style={"fontSize": "4rem"})
                          ]),
                          html.Div(className="progress progress-sm", children=[
                              html.Div(className="progress-bar", style={"width":f"{valor*10}%"}, role="progressbar")
                          ])
                          
                      ])]
    return card_children

def mapa_cidade(nome_municipio):
    sel = gdf[gdf["NM_MUN"] == nome_municipio]

    fig = go.Figure()

    fig.add_trace(
        go.Choropleth(
            geojson=sel.__geo_interface__,
            locations=sel.index,
            z=[1],                     
            featureidkey="id",
            colorscale=[[0, "#4C78A8"], [1, "#4C78A8"]],
            showscale=False,
            marker_line_color="black",
            marker_line_width=2
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
        modebar_remove=['zoom', 'pan', 'lasso', 'select', 'toImage']
    )
    return fig




@callback(
        Output("mapa-cidade", "figure"), 
        Output("card-irct","children"),
        Output("card-mitigacao","children"),
        Output("card-adaptacao","children"),
        Output("card-deficithabitacional","children"),
        Output("card-vulnerabilidadesocial","children"),
        Output("card-tabela-acoes","children"),
        Output("card-tabela-indicadores","children"),
        Input("dropdown-cidade", "value"))
def update_graph(value):
    dff = df[df['Município'] == value]
    
    # valores para os cards
    irct = round(dff['Índice de Resiliiência Climática e Territorial'].values[0],1)
    mitigacao = round(dff['Mitigação'].values[0],1)
    adaptacao = round(dff['Adaptação'].values[0],1)
    deficit = round(dff['Deficit Habitacional'].values[0],1)
    vulnerabilidade = round(dff['Vulnerabilidade Social'].values[0],1)

    #outputs dos cards
    irct = card_progress_irct(irct)
    mitigacao = card_progress_pequeno("Mitigação",mitigacao)
    adaptacao = card_progress_pequeno("Adaptação",adaptacao)
    deficit = card_progress_pequeno("Déficit Habitacional",deficit)
    vulnerabilidade = card_progress_pequeno("Vulnerabilidade Social",vulnerabilidade)

    #output do mapa
    mapa = mapa_cidade(value)

    #output das ações
    tabela_acoes = recomendacoes[recomendacoes['Município']==value][['Sugestões e Recomendações para Melhorias']]
    acoes = dag.AgGrid(
                        id="get-started-example-basic-df",
                        rowData=tabela_acoes.to_dict("records"),
                        columnDefs=[{"field": i} for i in tabela_acoes.columns],
                        style={"height": "250px"},
                        columnSize="sizeToFit",
                        columnSizeOptions={
                            'defaultMinWidth':100,
                            'columnLimits':[{'key':'Indicador','minWidth':200}]}
                    )
    
    #output dos indicadores
    dados_indicadores = dff.melt(id_vars="Município")
    dados_indicadores.columns = ["Município","Indicador","Valor"]
    dados_indicadores = dados_indicadores[["Indicador","Valor"]]
    indicadores =dag.AgGrid(
                        id="get-started-example-basic-df",
                        rowData=dados_indicadores.to_dict("records"),
                        columnDefs=[{"field": i} for i in dados_indicadores.columns],
                        style={"width": "100%"},
                        columnSize="sizeToFit",
                        columnSizeOptions={
                            'defaultMinWidth':100,
                            'columnLimits':[{'key':'Indicador','minWidth':200}]}
                    )

    return mapa, irct, mitigacao, adaptacao, deficit, vulnerabilidade, acoes, indicadores