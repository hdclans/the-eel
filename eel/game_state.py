from enum import Enum


class GameState(Enum):
    """États possibles du jeu"""
    MENU = "menu"
    PLAYING = "playing"
    WAITING_START = "waiting_start"
    GAME_OVER = "game_over"


class GameStateManager:
    """Gestionnaire d'états du jeu"""

    def __init__(self):
        self._state = GameState.MENU
        self._game_started = False

    @property
    def state(self):
        return self._state

    @property
    def is_menu(self):
        return self._state == GameState.MENU

    @property
    def is_playing(self):
        return self._state == GameState.PLAYING

    @property
    def is_waiting_start(self):
        return self._state == GameState.WAITING_START

    @property
    def is_game_over(self):
        return self._state == GameState.GAME_OVER

    @property
    def game_started(self):
        return self._game_started

    def transition_to(self, new_state):
        """Changer d'état"""
        self._state = new_state

    def start_game(self):
        """Démarrer le jeu"""
        self._state = GameState.WAITING_START
        self._game_started = False

    def begin_playing(self):
        """Commencer à jouer"""
        self._state = GameState.PLAYING
        self._game_started = True

    def game_over(self):
        """Terminer le jeu"""
        self._state = GameState.GAME_OVER

    def restart(self):
        """Redémarrer"""
        self._state = GameState.MENU
        self._game_started = False

    def should_update_game(self):
        """Le jeu doit-il être mis à jour ?"""
        return self.is_playing and self._game_started