from dash import Dash, html, page_container, page_registry
import dash_bootstrap_components as dbc
import os
import threading
import webbrowser


app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)
server = app.server



def _build_navigation() -> dbc.Nav:
    """Build page links from Dash's page registry using Bootstrap nav pills."""
    if not page_registry:
        return dbc.Nav(
            [dbc.NavItem(dbc.NavLink("Aucune page enregistree pour le moment.", disabled=True))],
            pills=True,
        )

    pages = sorted(
        page_registry.values(),
        key=lambda page: (page.get("order", 9999), page.get("path", "/")),
    )

    return dbc.Nav(
        [
            dbc.NavItem(
                dbc.NavLink(
                    page.get("name", page.get("module", "Page")),
                    href=page.get("path", "/"),
                    active="exact",
                )
            )
            for page in pages
        ],
        pills=True,
        className="gap-2 flex-wrap",
    )


app.layout = dbc.Container(
    [
        dbc.NavbarSimple(
            brand="Application M2 MECEN",
            color="primary",
            dark=True,
            fluid=True,
            className="rounded-3 shadow-sm mt-3",
        ),
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.Div(
                            [
                                html.H2("Navigation", className="h5 mb-3"),
                                _build_navigation(),
                            ]
                        )
                    ]
                )
            ],
            className="my-4 shadow-sm border-0",
        ),
        dbc.Card(
            dbc.CardBody(page_container, className="p-4"),
            className="shadow-sm border-0 mb-4",
        ),
    ],
    fluid="md",
    className="pb-4",
)


if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Timer(1, lambda: webbrowser.open("http://127.0.0.1:8050/table")).start()
    app.run(debug=True, use_reloader=True)
