# Eval Python Dash

## Structure du projet

- `app.py` : fichier principal qui lance l'application Dash.
- `pages/` : pages de l'application, avec separation layout/callbacks.
	- `table.py` : layout de la page 1 (menus deroulants + tableau).
	- `table_cb.py` : callbacks de la page 1 (filtrage region/type).
- `assets/` : fichiers CSS et ressources statiques.
- `datas/` : donnees source (`avocado.csv`).

## Installation

1. Creer un environnement virtuel (optionnel mais recommande).
2. Installer les dependances :

```bash
uv add dash
```

## Lancement

Depuis la racine du projet :

```bash
uv run app.py
```

