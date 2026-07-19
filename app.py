import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

from flask import render_template



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
        #head
        rendered = rendered.replace("<!--dash-metas-->", metas)
        rendered = rendered.replace("<!--dash-title-->", title)
        rendered = rendered.replace("<!--dash-css-->", css)
        rendered = rendered.replace("<!--dash-config-->", config)
        rendered = rendered.replace("<!--dash-scripts-->", scripts)
        rendered = rendered.replace("<!--dash-favicon-->", favicon)
        #onde vai o dash
        rendered = rendered.replace("<!--dash-app_entry-->", app_entry)
        #antes do /body
        rendered = rendered.replace("<!--dash-renderer-->", renderer)

        return rendered


app = CustomDash('base-site.html', use_pages=True)
app.title = "Índice de Resiliência Climática Territorial"


app.layout = [
    dash.page_container
]



if __name__ == "__main__":
    app.run(debug=True)
