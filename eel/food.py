import pygame
import random
from . import config


class Food:
    """Classe représentant la nourriture"""

    def __init__(self):
        self.x = 0
        self.y = 0
        self.generate()

    def generate(self, avoid_positions=None):
        """Générer une nouvelle position pour la nourriture"""
        if avoid_positions is None:
            avoid_positions = []

        # Générer position aléatoire
        self.x = random.randint(0, 10)
        self.y = random.randint(0, 10)

        # Éviter les positions occupées
        for avoid_x, avoid_y in avoid_positions:
            if self.x == avoid_x and self.y == avoid_y:
                self.generate(avoid_positions)  # Régénérer
                return

    def get_position(self):
        """Obtenir la position de la nourriture"""
        return (self.x, self.y)

    def draw(self, screen, grid_bounds):
        """Dessiner la nourriture"""
        food_pixel_x = grid_bounds.left + (self.x * config.CELL_SIZE) + (config.CELL_SIZE // 2)
        food_pixel_y = grid_bounds.top + (self.y * config.CELL_SIZE) + (config.CELL_SIZE // 2)
        pygame.draw.circle(screen, "red", (food_pixel_x, food_pixel_y), 8)