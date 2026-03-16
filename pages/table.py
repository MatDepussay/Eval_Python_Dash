import csv
from functools import lru_cache
from pathlib import Path

import dash_bootstrap_components as dbc
from dash import dash_table, dcc, html, register_page


register_page(__name__, path="/table", name="Table", order=1)

DATA_FILE = Path(__file__).resolve().parent.parent / "datas" / "avocado.csv"

DISPLAY_COLUMNS = [
    "Date",
    "AveragePrice",
    "Total Volume",
    "Total Bags",
    "type",
    "year",
    "region",
]

REGION_DROPDOWN_ID = "table-page-region-dd"
TYPE_DROPDOWN_ID = "table-page-type-dd"
DATA_TABLE_ID = "table-page-data-table"


@lru_cache(maxsize=1)
def _load_rows() -> list[dict]:
    """Load avocado dataset rows and keep only the required page-1 columns."""
    with DATA_FILE.open(mode="r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = []
        for row in reader:
            cleaned = {column: row.get(column, "") for column in DISPLAY_COLUMNS}
            rows.append(cleaned)
        return rows



def _build_dropdown_options(rows: list[dict], field_name: str, all_label: str) -> list[dict]:
    values = sorted({row[field_name] for row in rows if row.get(field_name)})
    options = [{"label": all_label, "value": "ALL"}]
    options.extend({"label": value, "value": value} for value in values)
    return options


_INITIAL_ROWS = _load_rows()
_COLUMNS = [{"name": column, "id": column} for column in DISPLAY_COLUMNS]


layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                [
                    html.H2("Page 1 - Tableau des donnees", className="mb-1"),
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
                                    html.Label("Selectionner une region", htmlFor=REGION_DROPDOWN_ID, className="form-label"),
                                    dcc.Dropdown(
                                        id=REGION_DROPDOWN_ID,
                                        options=_build_dropdown_options(_INITIAL_ROWS, "region", "Toutes les regions"),
                                        value="ALL",
                                        clearable=False,
                                    ),
                                ],
                                xs=12,
                                md=6,
                                className="mb-3 mb-md-0",
                            ),
                            dbc.Col(
                                [
                                    html.Label("Selectionner un type", htmlFor=TYPE_DROPDOWN_ID, className="form-label"),
                                    dcc.Dropdown(
                                        id=TYPE_DROPDOWN_ID,
                                        options=_build_dropdown_options(_INITIAL_ROWS, "type", "Tous les types"),
                                        value="ALL",
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
        dbc.Card(
            [
                dbc.CardHeader("Tableau", className="fw-semibold"),
                dbc.CardBody(
                    html.Div(
                        dash_table.DataTable(
                            id=DATA_TABLE_ID,
                            columns=_COLUMNS,
                            data=_INITIAL_ROWS,
                            page_size=15,
                            sort_action="native",
                            filter_action="none",
                            style_table={"overflowX": "auto"},
                            style_cell={
                                "textAlign": "left",
                                "padding": "0.75rem",
                                "fontFamily": 'var(--bs-body-font-family, "Segoe UI", sans-serif)',
                                "fontSize": "0.95rem",
                                "border": "1px solid var(--bs-border-color, #dee2e6)",
                                "backgroundColor": "var(--bs-body-bg, #ffffff)",
                                "color": "var(--bs-body-color, #212529)",
                                "minWidth": "110px",
                                "maxWidth": "260px",
                                "whiteSpace": "normal",
                                "height": "auto",
                            },
                            style_header={
                                "backgroundColor": "var(--bs-primary, #0d6efd)",
                                "color": "white",
                                "fontWeight": "700",
                                "border": "1px solid var(--bs-primary, #0d6efd)",
                            },
                            style_data_conditional=[
                                {"if": {"row_index": "odd"}, "backgroundColor": "var(--bs-tertiary-bg, #f8f9fa)"}
                            ],
                            css=[
                                {
                                    "selector": ".dash-spreadsheet-container .dash-spreadsheet-inner table",
                                    "rule": "border-collapse: collapse;",
                                },
                            ],
                        ),
                        className="table-responsive",
                    )
                ),
            ],
            className="shadow-sm border-0",
        ),
    ],
    fluid=True,
    className="px-0",
)


from pages import table_cb  # noqa: E402,F401
