# the-eel

Jeu Snake en Python avec Pygame, inspiré du Snake Google.

## Installation
```bash
pip install -r requirements.txt
```

## Lancement
```bash
python main.py
```

## Tests


### Lancer les tests
```bash
# Tests complets avec détails
python -m pytest tests/ -v

# Tests avec traceback court
python -m pytest tests/ -v --tb=short
```

### Structure des tests
- `test_eel.py` - Tests pour la classe Eel
- `test_game.py` - Tests pour la classe Game
- `test_food.py` - Tests pour la classe Food
- `test_grid.py` - Tests pour la classe Grid