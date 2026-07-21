import dash
from dash import html
import dash_ag_grid as dag

app = dash.Dash(__name__)

# 1. Format your data using standard Markdown syntax
data = [
    {"site": "[Google](https://google.com)", "category": "Search"},
    {"site": "[Plotly](javascript:alert('teste'))", "category": "Analytics"},
]

columnDefs = [
    {
        "field": "site",
        # 2. Tell AG Grid to process this column as markdown
        "cellRenderer": "markdown",
        # 3. Optional: Force the link to open in a new browser tab
        "linkTarget": "_self" 
    },
    {"field": "category"}
]

app.layout = html.Div([
    dag.AgGrid(
        rowData=data,
        columnDefs=columnDefs,
        id="grid-links"
    )
])

if __name__ == "__main__":
    app.run(debug=True)