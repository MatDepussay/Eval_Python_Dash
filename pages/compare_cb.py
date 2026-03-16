import csv
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
from datetime import datetime

from dash import Input, Output, callback
from plotly import graph_objects as go


DATA_FILE = Path(__file__).resolve().parent.parent / "datas" / "avocado.csv"


@lru_cache(maxsize=1)
def _rows() -> list[dict]:
    with DATA_FILE.open(mode="r", encoding="utf-8", newline="") as csv_file:
        return list(csv.DictReader(csv_file))


def _region_series(region: str) -> tuple[list[str], list[float]]:
    region_rows = [row for row in _rows() if row.get("region") == region]

    by_date = defaultdict(list)
    for row in region_rows:
        date_value = row.get("Date")
        price_value = row.get("AveragePrice")
        if not date_value or not price_value:
            continue
        try:
            by_date[date_value].append(float(price_value))
        except ValueError:
            continue

    dates = sorted(by_date.keys())
    average_prices = [sum(by_date[date]) / len(by_date[date]) for date in dates]
    return dates, average_prices


def _build_region_figure(region: str, x_range: list | None = None, y_range: list | None = None) -> go.Figure:
    dates, average_prices = _region_series(region)

    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=dates,
            y=average_prices,
            mode="lines",
            line={"color": "#1f77b4", "width": 2},
            name=region,
        )
    )
    figure.update_layout(
        title=f"Evolution du prix moyen - {region}",
        xaxis_title="Date",
        yaxis_title="Prix moyen",
        template="plotly_white",
        margin={"l": 40, "r": 20, "t": 55, "b": 40},
        height=420,
    )
    if x_range:
        figure.update_xaxes(range=x_range)
    if y_range:
        figure.update_yaxes(range=y_range)

    return figure


def _shared_ranges(left_region: str, right_region: str) -> tuple[list | None, list | None]:
    left_dates, left_prices = _region_series(left_region) if left_region else ([], [])
    right_dates, right_prices = _region_series(right_region) if right_region else ([], [])

    all_dates = left_dates + right_dates
    all_prices = left_prices + right_prices

    if not all_dates or not all_prices:
        return None, None

    parsed_dates = [datetime.fromisoformat(date_text) for date_text in all_dates]
    x_range = [min(parsed_dates), max(parsed_dates)]

    min_price = min(all_prices)
    max_price = max(all_prices)
    if min_price == max_price:
        pad = max(0.1, max_price * 0.05)
    else:
        pad = (max_price - min_price) * 0.05
    y_range = [min_price - pad, max_price + pad]

    return x_range, y_range


@callback(
    Output("compare-left-figure", "figure"),
    Output("compare-right-figure", "figure"),
    Input("compare-region-left-dd", "value"),
    Input("compare-region-right-dd", "value"),
)
def update_compare_figures(left_region: str, right_region: str):
    x_range, y_range = _shared_ranges(left_region, right_region)
    left_figure = _build_region_figure(left_region, x_range=x_range, y_range=y_range) if left_region else go.Figure()
    right_figure = _build_region_figure(right_region, x_range=x_range, y_range=y_range) if right_region else go.Figure()
    return left_figure, right_figure