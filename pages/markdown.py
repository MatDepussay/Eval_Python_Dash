from functools import lru_cache
from pathlib import Path

from dash import dcc, html, register_page


register_page(__name__, path="/markdown", name="MarkDown", order=3)

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


@lru_cache(maxsize=1)
def _read_markdown(filename: str) -> str:
    file_path = ASSETS_DIR / filename
    return file_path.read_text(encoding="utf-8")


def _accordion_section(title: str, filename: str, opened: bool = False) -> html.Details:
    summary_background = "#c8d8ef" if opened else "#f8f8f8"

    return html.Details(
        [
            html.Summary(
                title,
                style={
                    "fontWeight": "600",
                    "cursor": "pointer",
                    "backgroundColor": summary_background,
                    "padding": "0.55rem 0.75rem",
                    "fontSize": "14px",
                },
            ),
            dcc.Markdown(
                _read_markdown(filename),
                style={"padding": "0.9rem 0.75rem 0.6rem"},
            ),
        ],
        open=opened,
        style={
            "backgroundColor": "#ffffff",
            "border": "1px solid #d0d0d0",
            "borderRadius": "4px",
            "overflow": "hidden",
        },
    )


layout = html.Div(
    [
        html.Div(
            html.H2(
                "Presentation de Dash",
                style={
                    "margin": "0",
                    "color": "#ffffff",
                    "textTransform": "uppercase",
                    "letterSpacing": "1px",
                    "fontSize": "34px",
                    "textAlign": "center",
                    "textShadow": "0 1px 3px rgba(0, 0, 0, 0.45)",
                },
            ),
            style={
                "backgroundImage": "url('/assets/dash.jpg')",
                "backgroundSize": "cover",
                "backgroundPosition": "center",
                "borderRadius": "4px 4px 0 0",
                "height": "88px",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
                "borderBottom": "1px solid #c8c8c8",
            },
        ),
        html.Div(
            [
                _accordion_section("Accueil", "expli1.md"),
                _accordion_section("Layout", "expli2.md"),
                _accordion_section("CallBack", "expli3.md"),
            ],
            style={"display": "grid", "gap": "0.55rem", "padding": "0.75rem"},
        ),
    ],
    style={
        "backgroundColor": "#f1f1f1",
        "padding": "0.85rem",
        "borderRadius": "10px",
        "border": "2px solid #5d5d5d",
        "boxShadow": "12px 10px 0 #7a7a7a",
    },
)