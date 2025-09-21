# the-eel

Jeu Snake simple en Python avec Pygame, inspiré du Snake Google.

**Note:** Première version fonctionnelle réalisée en Python. En raison de complications pour la mise en ligne, une migration vers JavaScript est prévue dans un autre repository.

## Fonctionnalités
- Jeu Snake fonctionnel
- Différentes vitesses de jeu
- Interface simple et intuitive

## Prérequis
- Python 3.7 ou supérieur
- pip (gestionnaire de packages Python)

## Installation

1. Cloner le repository
```bash
git clone https://github.com/hdclans/the-eel.git
cd the-eel
```

2. Installer Python (si pas déjà installé)
   - Télécharger depuis https://python.org
   - Ou via gestionnaire de packages selon votre OS

3. Installer les dépendances
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