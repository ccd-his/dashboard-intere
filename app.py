from dash import Dash, dcc, callback, Output, Input
from dash_template_rendering import TemplateRenderer, render_dash_template_string
import plotly.express as px
import pandas as pd

df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv"
)

app = Dash(__name__,
           assets_external_path="https://cdn.jsdelivr.net/npm/@tabler/core@1.4.0/dist/css/tabler.min.css")
TemplateRenderer(dash=app)
app.scripts.config.serve_locally = False

with open("layout.html","r", encoding="utf-8") as file:
    layout_string = file.read()

app.layout = render_dash_template_string(
    layout_string,
    #dropdown=dcc.Dropdown(df.country.unique(), "Brazil", id="dropdown-selection"),
    #graph=dcc.Graph(id="graph-content"),
)


@callback(Output("graph-content", "figure"), Input("dropdown-selection", "value"))
def update_graph(value):
    dff = df[df.country == value]
    return px.line(dff, x="year", y="pop")


if __name__ == "__main__":
    app.run(debug=True)