from dash import html


def make_avatar(text, color="blue"):
    return html.Span(text, className=f"avatar bg-{color}-lt")


def make_table(id, headers, rows, header_classes, content_classes):
    return make_card(
        html.Div(
            className="table-responsive",
            children=[
                html.Table(
                    className="table table-vcenter card-table",
                    children=[
                        html.Thead(
                            html.Tr(
                                [
                                    html.Th(header, className=header_classes[index])
                                    for index, header in enumerate(headers)
                                ],
                            )
                        ),
                        html.Tbody(
                            [
                                html.Tr(
                                    [
                                        html.Td(
                                            cell,
                                            className=content_classes[index],
                                        )
                                        for index, cell in enumerate(row)
                                    ]
                                )
                                for row in rows
                            ]
                        ),
                    ],
                )
            ],
        )
    )


def make_card(children):
    return html.Div(children, className="card")


def make_title(title, overtitle, filters):
    return html.Div(
        className="row mb-2 mt-4",
        children=[
            html.Div(
                className="col-md-10 col-sm-12",
                children=[
                    html.Div(className="page-pretitle", children=overtitle),
                    html.H1(
                        className="page-title",
                        children=title,
                    ),
                ],
            ),
            html.Div(className="col-md-2 col-sm-12", children=filters),
        ],
    )
