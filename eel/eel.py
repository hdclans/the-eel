import pygame
from . import config


class Eel:
    """Classe représentant l'anguille"""

    def __init__(self, start_x=5, start_y=5):
        # Position en coordonnées de grille
        self.grid_x = start_x
        self.grid_y = start_y
        self.target_grid_x = start_x
        self.target_grid_y = start_y

        # Direction et mouvement
        self.auto_direction = pygame.Vector2(1, 0)
        self.pending_direction = None
        self.move_timer = 0
        self.first_move = True
        self.body_delay = 0.05
        self.body_move_timer = 0

        # Corps de l'anguille
        self.body = []
        self.body_history = []
        self.initial_segments_to_add = 3
        self.segments_added = 0

    def add_segment(self):
        """Ajouter un nouveau segment au corps"""
        positions_per_cell = int(config.MOVE_INTERVAL * config.FPS)
        new_segment_index = len(self.body) * positions_per_cell + positions_per_cell

        if len(self.body_history) > new_segment_index:
            self.body.append((self.body_history[-new_segment_index][0], self.body_history[-new_segment_index][1]))
        else:
            self.body.append((-10, -10))

    def update_movement(self, dt):
        """Mettre à jour le mouvement de l'anguille"""
        self.move_timer += dt
        self.body_move_timer += dt

        # Ajouter position actuelle à l'historique
        if self.body_move_timer >= self.body_delay:
            self.body_history.append((self.grid_x, self.grid_y))

        # Ajouter progressivement les segments initiaux
        if self.segments_added < self.initial_segments_to_add and self.body_move_timer >= self.body_delay:
            if len(self.body_history) >= (self.segments_added + 1) * int(config.MOVE_INTERVAL * config.FPS):
                self.add_segment()
                self.segments_added += 1

        # Changement de direction et mouvement synchronisés
        if self.move_timer >= config.MOVE_INTERVAL:
            self.move_timer -= config.MOVE_INTERVAL

            # Appliquer changement de direction si valide
            if self.pending_direction and self._is_valid_direction_change(self.pending_direction):
                self.auto_direction = self.pending_direction
                self.pending_direction = None

            # Mouvement
            if self.first_move:
                self.first_move = False
                self.target_grid_x = 5 + self.auto_direction.x
                self.target_grid_y = 5 + self.auto_direction.y
            else:
                self.target_grid_x += self.auto_direction.x
                self.target_grid_y += self.auto_direction.y

        # Mettre à jour positions des segments
        self._update_body_segments()

        # mouvement fluide
        self._interpolate_position()

        # Limiter taille historique
        self._limit_history()

    def _update_body_segments(self):
        """Mettre à jour les positions des segments du corps"""
        positions_per_cell = int(config.MOVE_INTERVAL * config.FPS)

        for i in range(len(self.body)):
            history_index = len(self.body_history) - 1 - (i + 1) * positions_per_cell
            if history_index >= 0:
                self.body[i] = self.body_history[history_index]

    def _interpolate_position(self):
        """Interpolation fluide vers la position cible"""
        progress = self.move_timer / config.MOVE_INTERVAL
        progress = min(progress, 1.0)

        if self.first_move:
            self.grid_x = 5
            self.grid_y = 5
        else:
            start_x = self.target_grid_x - self.auto_direction.x
            start_y = self.target_grid_y - self.auto_direction.y

            self.grid_x = start_x + (self.target_grid_x - start_x) * progress
            self.grid_y = start_y + (self.target_grid_y - start_y) * progress

    def _limit_history(self):
        """Limiter la taille de l'historique"""
        positions_per_cell = int(config.MOVE_INTERVAL * config.FPS)
        max_history = len(self.body) * positions_per_cell + 100
        if len(self.body_history) > max_history:
            self.body_history = self.body_history[-max_history:]

    def _is_valid_direction_change(self, new_direction):
        """Vérifier si le changement de direction est valide (pas de demi-tour)"""
        return new_direction != -self.auto_direction

    def set_pending_direction(self, direction):
        """Définir la direction en attente"""
        self.pending_direction = direction

    def start_movement(self, direction):
        """Démarrer le mouvement - toujours une case à droite puis direction du clic"""
        if self.first_move:
            self.auto_direction = pygame.Vector2(1, 0)  # Toujours commencer vers la droite
            self.pending_direction = direction

    def get_head_position(self):
        """Obtenir la position de la tête en coordonnées de grille"""
        return (int(round(self.grid_x)), int(round(self.grid_y)))

    def check_self_collision(self):
        """Vérifier collision avec soi-même"""
        current_grid_x, current_grid_y = self.get_head_position()

        # Vérifier seulement quand proche d'une position entière
        if abs(self.grid_x - round(self.grid_x)) < 0.1 and abs(self.grid_y - round(self.grid_y)) < 0.1:
            for i, segment in enumerate(self.body):
                segment_grid_x = int(round(segment[0]))
                segment_grid_y = int(round(segment[1]))

                # Ignorer segments hors grille
                if (0 <= segment_grid_x < 11 and 0 <= segment_grid_y < 11 and
                    current_grid_x == segment_grid_x and current_grid_y == segment_grid_y):
                    return True
        return False

    def is_out_of_bounds(self):
        """Vérifier si l'anguille sort des limites"""
        return not (0 <= self.target_grid_x < 11 and 0 <= self.target_grid_y < 11)

    def get_pixel_position(self, grid_bounds):
        """Convertir position grille en pixels"""
        pixel_x = grid_bounds.left + (self.grid_x * config.CELL_SIZE) + (config.CELL_SIZE // 2)
        pixel_y = grid_bounds.top + (self.grid_y * config.CELL_SIZE) + (config.CELL_SIZE // 2)
        return pygame.Vector2(pixel_x, pixel_y)

    def draw(self, screen, grid_bounds):
        """Dessiner l'anguille"""
        # Dessiner les segments du corps
        for segment_pos in self.body:
            segment_pixel_x = grid_bounds.left + (segment_pos[0] * config.CELL_SIZE) + (config.CELL_SIZE // 2)
            segment_pixel_y = grid_bounds.top + (segment_pos[1] * config.CELL_SIZE) + (config.CELL_SIZE // 2)
            pygame.draw.circle(screen, config.PLAYER_COLOR, (segment_pixel_x, segment_pixel_y), config.PLAYER_RADIUS)

        # Dessiner la tête
        pixel_pos = self.get_pixel_position(grid_bounds)
        pygame.draw.circle(screen, config.PLAYER_COLOR, pixel_pos, config.PLAYER_RADIUS)