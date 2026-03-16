from dash import Dash, dcc, html, page_container, page_registry
import os
import threading
import webbrowser


app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)
server = app.server


def _build_navigation() -> list:
    """Build visible navigation links for the two required pages."""
    page_names = {page.get("name") for page in page_registry.values()}

    links = [
        dcc.Link("Table", href="/table", style={"display": "inline-block", "marginRight": "1rem"}),
        dcc.Link("Compare", href="/compare", style={"display": "inline-block", "marginRight": "1rem"}),
    ]

    if "Table" not in page_names or "Compare" not in page_names:
        links.append(html.Span("(attention: une page n'est pas chargee)", style={"color": "#b00020"}))

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
