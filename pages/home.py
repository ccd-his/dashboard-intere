import dash
import plotly.graph_objects as go
from dash import Input, Output, callback, dcc, html

from data_source import (
    get_simplified_geometry,
    load_df_indicadores,
    load_df_irct_filtrado,
    load_gdf,
    load_df_textos_home,
)

dash.register_page(__name__, path="/")


layout = [
    # html.H3(children="IRCT", style={"textAlign": "right"}),
    html.Div(
        className="row mb-2 mt-4",
        children=[
            html.Div(
                id="titulo",
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
                id="texto-explicativo", className="col-lg-12 col-sm-12", children=[]
            ),
            html.Div(
                className="col-lg-12 col-sm-12",
                children=[
                    html.Div(
                        className="card h-100",
                        children=[
                            dcc.Loading(
                                dcc.Graph(
                                    id="mapa-indice",
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
    html.Div(id="click", children=[dcc.Location(id="url-loc")]),
]


def mapa_indice(indice):
    gdf = load_gdf()
    gdf_filtrado = load_df_irct_filtrado(load_df_indicadores())

    fig = go.Figure()

    fig.add_trace(
        go.Choropleth(
            geojson=get_simplified_geometry(gdf, background=True),
            locations=gdf.index,
            z=[1] * len(gdf),
            colorscale=[[0, "lightgray"], [1, "lightgray"]],
            showscale=False,
            marker_line_color="white",
            marker_line_width=0.5,
            hoverinfo="skip",
        )
    )

    fig.add_trace(
        go.Choropleth(
            geojson=get_simplified_geometry(gdf_filtrado),
            locations=gdf_filtrado.index,
            z=gdf_filtrado[indice],
            colorscale="Viridis_r",
            marker_line_color="white",
            marker_line_width=0.5,
            colorbar_title="Índice",
            colorbar={"orientation": "h", "y": -0.15},
            text=gdf_filtrado["NM_MUN"],
            hovertemplate=("<b>%{text}</b><br>Índice: %{z:.2f}<extra></extra>"),
        )
    )

    xmin, ymin, xmax, ymax = gdf_filtrado.total_bounds

    dx = (xmax - xmin) * 0.10
    dy = (ymax - ymin) * 0.20

    fig.update_geos(
        visible=False,
        lonaxis_range=[xmin - dx, xmax + dx],
        lataxis_range=[ymin - dy, ymax + dy],
    )

    fig.update_layout(
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        paper_bgcolor="white",
        plot_bgcolor="white",
        height=650,
    )

    return fig


def texto_explicativo(indice):
    textos = load_df_textos_home()
    paragrafo = textos[textos["Índice"]==indice]['Texto']
    
    return dcc.Markdown(paragrafo)


@callback(
    Output("mapa-indice", "figure"),
    Output("titulo", "children"),
    Output("texto-explicativo", "children"),
    Input("dropdown-indice", "value"),
)
def update_graph(value):

    # output do mapa
    mapa = mapa_indice(value)

    # output do título

    titulo = [
        html.Div(className="page-pretitle", children="Home"),
        html.H1(className="page-title", children=value),
    ]

    # output do texto
    texto = texto_explicativo(value)
    return mapa, titulo, texto


@callback(
    Output("url-loc", "href"),
    Input("mapa-indice", "clickData"),
    prevent_initial_call=True,
)
def update_click(clickData):

    return f"./cidades#{clickData['points'][0]['text']}"

