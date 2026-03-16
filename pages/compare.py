import csv
from functools import lru_cache
from pathlib import Path

import dash_bootstrap_components as dbc
from dash import dcc, html, register_page


register_page(__name__, path="/compare", name="Compare", order=2)

DATA_FILE = Path(__file__).resolve().parent.parent / "datas" / "avocado.csv"

LEFT_REGION_DROPDOWN_ID = "compare-region-left-dd"
RIGHT_REGION_DROPDOWN_ID = "compare-region-right-dd"
LEFT_GRAPH_ID = "compare-left-figure"
RIGHT_GRAPH_ID = "compare-right-figure"


@lru_cache(maxsize=1)
def _region_options() -> list[dict]:
    with DATA_FILE.open(mode="r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        regions = sorted({row.get("region", "") for row in reader if row.get("region")})
    return [{"label": region, "value": region} for region in regions]


_REGION_OPTIONS = _region_options()
_DEFAULT_LEFT_REGION = _REGION_OPTIONS[0]["value"] if _REGION_OPTIONS else None
_DEFAULT_RIGHT_REGION = _REGION_OPTIONS[1]["value"] if len(_REGION_OPTIONS) > 1 else _DEFAULT_LEFT_REGION


layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                [
                    html.H2("Page 2 - Comparaison des regions", className="mb-1"),
                ],
                width=12,
            ),
            className="mb-4",
        ),
        dbc.Card(
            [
                dbc.CardHeader("Filtres", className="fw-semibold"),
                dbc.CardBody(
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Label("Region 1", htmlFor=LEFT_REGION_DROPDOWN_ID, className="form-label"),
                                    dcc.Dropdown(
                                        id=LEFT_REGION_DROPDOWN_ID,
                                        options=_REGION_OPTIONS,
                                        value=_DEFAULT_LEFT_REGION,
                                        clearable=False,
                                    ),
                                ],
                                xs=12,
                                md=6,
                                className="mb-3 mb-md-0",
                            ),
                            dbc.Col(
                                [
                                    html.Label("Region 2", htmlFor=RIGHT_REGION_DROPDOWN_ID, className="form-label"),
                                    dcc.Dropdown(
                                        id=RIGHT_REGION_DROPDOWN_ID,
                                        options=_REGION_OPTIONS,
                                        value=_DEFAULT_RIGHT_REGION,
                                        clearable=False,
                                    ),
                                ],
                                xs=12,
                                md=6,
                            ),
                        ],
                        className="g-3",
                    )
                ),
            ],
            className="shadow-sm border-0 mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Region 1", className="fw-semibold"),
                            dbc.CardBody(dcc.Graph(id=LEFT_GRAPH_ID, config={"displaylogo": False})),
                        ],
                        className="shadow-sm border-0 h-100",
                    ),
                    xs=12,
                    lg=6,
                    className="mb-4 mb-lg-0",
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Region 2", className="fw-semibold"),
                            dbc.CardBody(dcc.Graph(id=RIGHT_GRAPH_ID, config={"displaylogo": False})),
                        ],
                        className="shadow-sm border-0 h-100",
                    ),
                    xs=12,
                    lg=6,
                ),
            ],
            className="g-4",
        ),
    ],
    fluid=True,
    className="px-0",
)


from pages import compare_cb  # noqa: E402,F401
