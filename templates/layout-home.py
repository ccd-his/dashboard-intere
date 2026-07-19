[
    html.H1(children="Title of Dash App", style={"textAlign": "center"}),
    dcc.Dropdown(df.country.unique(), "Canada", id="dropdown-selection"),
    dcc.Graph(id="graph-content"),
]