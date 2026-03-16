# Eval Python Dash

Application Dash multipage (M2 MECEN) basee sur le jeu de donnees avocado.

## Fonctionnalites

- Navigation dynamique entre les pages via la barre de navigation.
- Page `Table` : affichage tabulaire avec filtres par region et type.
- Page `Compare` : comparaison graphique de deux regions (prix moyen dans le temps).
- Page `MarkDown` : contenu pedagogique Dash affiche dans un accordion.

## Prerequis

- Python 3.12+
- `uv` installe sur la machine

## Installation

Depuis la racine du projet :

```bash
uv sync
```

Cette commande installe les dependances definies dans [pyproject.toml](pyproject.toml).

## Lancement

Toujours depuis la racine du projet :

```bash
uv run app.py
```

L'application est accessible sur :

- http://127.0.0.1:8050/

## Routes principales

- `/table` : tableau avec filtres
- `/compare` : comparaison de regions
- `/markdown` : contenu explicatif

## Structure du projet

- `app.py` : point d'entree de l'application Dash, layout global et navigation.
- `pyproject.toml` : metadonnees projet et dependances.
- `datas/avocado.csv` : jeu de donnees source.
- `assets/` : ressources statiques (images et fichiers markdown).
- `pages/` : pages Dash et callbacks associes.

Dans `pages/` :

- `table.py` : layout de la page tableau.
- `table_cb.py` : callbacks de filtrage du tableau.
- `compare.py` : layout de la page de comparaison.
- `compare_cb.py` : callbacks de generation des graphiques.
- `markdown.py` : layout de la page markdown.

## Dependances principales

- `dash`
- `dash-bootstrap-components`

