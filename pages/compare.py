import csv
from functools import lru_cache
from pathlib import Path

from dash import dcc, html, register_page


register_page(__name__, path="/compare", name="Compare")

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


layout = html.Div(
	[
		html.H2("Page 2 - Comparaison des regions"),
		html.Div(
			[
				html.Div(
					[
						html.Label("Region 1"),
						dcc.Dropdown(
							id=LEFT_REGION_DROPDOWN_ID,
							options=_REGION_OPTIONS,
							value=_DEFAULT_LEFT_REGION,
							clearable=False,
						),
					],
					style={"flex": "1", "minWidth": "280px"},
				),
				html.Div(
					[
						html.Label("Region 2"),
						dcc.Dropdown(
							id=RIGHT_REGION_DROPDOWN_ID,
							options=_REGION_OPTIONS,
							value=_DEFAULT_RIGHT_REGION,
							clearable=False,
						),
					],
					style={"flex": "1", "minWidth": "280px"},
				),
			],
			style={"display": "flex", "gap": "1rem", "flexWrap": "wrap", "marginBottom": "1rem"},
		),
		html.Div(
			[
				html.Div(
					dcc.Graph(id=LEFT_GRAPH_ID, config={"displaylogo": False}),
					style={"flex": "1", "minWidth": "320px"},
				),
				html.Div(
					dcc.Graph(id=RIGHT_GRAPH_ID, config={"displaylogo": False}),
					style={"flex": "1", "minWidth": "320px"},
				),
			],
			style={"display": "flex", "gap": "1rem", "flexWrap": "wrap"},
		),
	],
	style={"backgroundColor": "#efefef", "padding": "1rem", "borderRadius": "8px"},
)


# Import callbacks so they are registered when this page module is loaded.
from pages import compare_cb  # noqa: E402,F401
