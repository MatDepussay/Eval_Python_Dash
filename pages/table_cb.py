import csv
from functools import lru_cache
from pathlib import Path

from dash import Input, Output, callback


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


@lru_cache(maxsize=1)
def _load_rows() -> list[dict]:
    with DATA_FILE.open(mode="r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = []
        for row in reader:
            cleaned = {column: row.get(column, "") for column in DISPLAY_COLUMNS}
            rows.append(cleaned)
        return rows


@callback(
    Output("table-page-data-table", "data"),
    Input("table-page-region-dd", "value"),
    Input("table-page-type-dd", "value"),
)
def update_table_data(selected_region: str, selected_type: str) -> list[dict]:
    rows = _load_rows()

    if selected_region and selected_region != "ALL":
        rows = [row for row in rows if row.get("region") == selected_region]

    if selected_type and selected_type != "ALL":
        rows = [row for row in rows if row.get("type") == selected_type]

    return rows