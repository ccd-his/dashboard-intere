from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

from flask import render_template

df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv"
)


class CustomDash(Dash):

    def __init__(self, template, **kwargs):
        super().__init__(**kwargs)
        self.template = template
    def interpolate_index(
        self,
        metas: str = "",
        title: str = "",
        css: str = "",
        config: str = "",
        scripts: str = "",
        app_entry: str = "",
        favicon: str = "",
        renderer: str = "",
    ) -> str:
        rendered: str = render_template(self.template, title="<!--dash-title-->")

        rendered = rendered.replace("<!--dash-metas-->", metas)
        rendered = rendered.replace("<!--dash-title-->", title)
        rendered = rendered.replace("<!--dash-css-->", css)
        rendered = rendered.replace("<!--dash-config-->", config)
        rendered = rendered.replace("<!--dash-scripts-->", scripts)
        rendered = rendered.replace("<!--dash-app_entry-->", app_entry)
        rendered = rendered.replace("<!--dash-favicon-->", favicon)
        rendered = rendered.replace("<!--dash-renderer-->", renderer)

        return rendered


app = CustomDash('base-site.html')

# Requires Dash 2.17.0 or later
app.layout = [
    html.H1(children="Title of Dash App", style={"textAlign": "center"}),
    dcc.Dropdown(df.country.unique(), "Canada", id="dropdown-selection"),
    dcc.Graph(id="graph-content"),
]


@callback(Output("graph-content", "figure"), Input("dropdown-selection", "value"))
def update_graph(value):
    dff = df[df.country == value]
    return px.line(dff, x="year", y="pop")


if __name__ == "__main__":
    app.run(debug=True)
