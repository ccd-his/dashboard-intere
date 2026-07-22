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

df_irct = df[['Código IBGE','Município','Mitigação','Adaptação','Deficit Habitacional','Vulnerabilidade Social','Índice de Resiliiência Climática e Territorial']]
df_irct['Código IBGE'] = df_irct['Código IBGE'].astype('str')
gdf = gdf.merge(df_irct, left_on='CD_MUN',right_on='Código IBGE')


layout = [
    # html.H3(children="IRCT", style={"textAlign": "right"}),
    html.Div(
        className="row mb-2 mt-4",children=[
            html.Div(id="titulo",
                className="col-10",children=[
                    html.Div(
                        className="page-pretitle",children="Home"
                    ),
                    html.H1(
                        className="page-title",children="Índice de Resiliência Climática e Territorial"
                    ),
                ],
            ),

            html.Div(
                className="col-2",children=[
                    dcc.Dropdown(
                        options=[
                            "Índice de Resiliiência Climática e Territorial",
                            "Mitigação",
                            "Adaptação",
                            "Deficit Habitacional",
                            "Vulnerabilidade Social",
                        ],
                        value="Índice de Resiliiência Climática e Territorial",
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
                className="col-12",children=[
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
        ])
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
            text=gdf.NM_MUN,
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
        height=800,
    )
    return fig


@callback(
        Output("mapa-indice", "figure"), 
        Output("titulo",'children'),
        Input("dropdown-indice", "value"))
def update_graph(value):

    #output do mapa
    mapa = mapa_indice(value)

    #output do título
    if value == "Índice de Resiliiência Climática e Territorial":
        valor = "Índice de Resiliência Climática e Territorial"
    else:
        valor = value
    titulo= [
                    html.Div(
                        className="page-pretitle",children="Home"
                    ),
                    html.H1(
                        className="page-title",children=valor
                    ),
                ]

    return mapa, titulo