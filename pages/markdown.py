from functools import lru_cache
from pathlib import Path

import dash_bootstrap_components as dbc
from dash import dcc, html, register_page


register_page(__name__, path="/markdown", name="MarkDown", order=3)

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


@lru_cache(maxsize=1)
def _read_markdown(filename: str) -> str:
    file_path = ASSETS_DIR / filename
    return file_path.read_text(encoding="utf-8")


layout = dbc.Container(
    [
        dbc.Card(
            [
                html.Div(
                    html.H2(
                        "Presentation de Dash",
                        className="display-6 text-white text-center mb-0",
                    ),
                    style={
                        "backgroundImage": "url('/assets/dash.jpg')",
                        "backgroundSize": "cover",
                        "backgroundPosition": "center",
                        "minHeight": "140px",
                    },
                    className="d-flex align-items-center justify-content-center rounded-top px-3",
                ),
                dbc.CardBody(
                    [
                        dbc.Accordion(
                            [
                                dbc.AccordionItem(
                                    dcc.Markdown(_read_markdown("expli1.md"), className="mb-0"),
                                    title="Accueil",
                                    item_id="accueil",
                                ),
                                dbc.AccordionItem(
                                    dcc.Markdown(_read_markdown("expli2.md"), className="mb-0"),
                                    title="Layout",
                                    item_id="layout",
                                ),
                                dbc.AccordionItem(
                                    dcc.Markdown(_read_markdown("expli3.md"), className="mb-0"),
                                    title="CallBack",
                                    item_id="callback",
                                ),
                            ],
                            start_collapsed=True,
                            always_open=True,
                            className="shadow-sm",
                        ),
                    ]
                ),
            ],
            className="shadow-sm border-0",
        )
    ],
    fluid=True,
    className="px-0",
)
