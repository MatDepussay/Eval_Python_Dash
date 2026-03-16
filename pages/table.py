import csv
from functools import lru_cache
from pathlib import Path

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


layout = html.Div(
    [
        html.H2("Page 1 - Tableau des donnees"),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Selectionner une region:"),
                        dcc.Dropdown(
                            id=REGION_DROPDOWN_ID,
                            options=_build_dropdown_options(_INITIAL_ROWS, "region", "Toutes les regions"),
                            value="ALL",
                            clearable=False,
                        ),
                    ],
                    style={"minWidth": "280px", "flex": "1"},
                ),
                html.Div(
                    [
                        html.Label("Selectionner un type:"),
                        dcc.Dropdown(
                            id=TYPE_DROPDOWN_ID,
                            options=_build_dropdown_options(_INITIAL_ROWS, "type", "Tous les types"),
                            value="ALL",
                            clearable=False,
                        ),
                    ],
                    style={"minWidth": "280px", "flex": "1"},
                ),
            ],
            style={"display": "flex", "gap": "1rem", "flexWrap": "wrap", "marginBottom": "1rem"},
        ),
        dash_table.DataTable(
            id=DATA_TABLE_ID,
            columns=_COLUMNS,
            data=_INITIAL_ROWS,
            page_size=15,
            style_table={"overflowX": "auto", "border": "2px solid #000", "borderRadius": "0"},
            style_cell={
                "textAlign": "left",
                "padding": "0.5rem",
                "fontFamily": "Segoe UI, Tahoma, sans-serif",
                "fontSize": "14px",
                "minWidth": "110px",
                "maxWidth": "260px",
                "border": "1px solid #000",
            },
            style_header={
                "backgroundColor": "#87CEEB",
                "color": "#000000",
                "fontWeight": "600",
            },
            style_data={"backgroundColor": "#ffffff", "color": "#202124"},
            style_data_conditional=[
                {
                    "if": {"row_index": "odd"},
                    "backgroundColor": "#f2f2f2",
                }
            ],
            sort_action="native",
            filter_action="none",
        ),
    ],
    style={"backgroundColor": "#efefef", "padding": "1rem", "borderRadius": "8px"},
)


# Import callbacks so they are registered when this page module is loaded.
from pages import table_cb  # noqa: E402,F401