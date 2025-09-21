import pygame
from . import config


class Grid:
    """Classe pour gérer l'affichage de la grille"""

    def __init__(self, screen_center):
        self.screen_center = screen_center
        self.bounds = None
        self._create_bounds()

    def _create_bounds(self):
        """Créer les limites de la grille"""
        rect_width = 605
        rect_height = 605

        self.bounds = pygame.Rect(0, 0, rect_width - 1, rect_height - 1)
        self.bounds.center = self.screen_center

    def get_bounds(self):
        """Obtenir les limites de la grille"""
        return self.bounds

    def draw(self, screen, cell_size):
        """Dessiner la grille"""
        # Lignes verticales
        for x in range(self.bounds.left, self.bounds.right + 1, cell_size):
            pygame.draw.line(
                screen, "darkgrey",
                (x, self.bounds.top), (x, self.bounds.bottom), 1
            )

        # Lignes horizontales
        for y in range(self.bounds.top, self.bounds.bottom + 1, cell_size):
            pygame.draw.line(
                screen, "darkgrey",
                (self.bounds.left, y), (self.bounds.right, y), 1
            )

        # Bord rouge
        pygame.draw.rect(screen, "red", self.bounds, 3)