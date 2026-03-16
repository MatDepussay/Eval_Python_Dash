from dash import Dash, dcc, html, page_container, page_registry
import os
import threading
import webbrowser


app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)
server = app.server


def _build_navigation() -> list:
    """Build page links from Dash's page registry."""
    if not page_registry:
        return [html.P("Aucune page enregistree pour le moment.")]

    pages = sorted(
        page_registry.values(),
        key=lambda page: (page.get("order", 9999), page.get("path", "/")),
    )
    links = []
    for page in pages:
        links.append(
            dcc.Link(
                page.get("name", page.get("module", "Page")),
                href=page.get("path", "/"),
                style={"display": "inline-block", "marginRight": "1rem"},
            )
        )
    return links


app.layout = html.Div(
    [
        html.H1("Application Dash"),
        html.Nav(_build_navigation(), style={"marginBottom": "1rem"}),
        page_container,
    ],
    style={"maxWidth": "1000px", "margin": "0 auto", "padding": "1.5rem"},
)


if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Timer(1, lambda: webbrowser.open("http://127.0.0.1:8050/table")).start()
    app.run(debug=True, use_reloader=True)
