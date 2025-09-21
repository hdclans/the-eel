import pygame
from . import config


class Menu:
    """Classe pour gérer le menu principal et game over"""

    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.selected_speed = config.SPEED_NORMAL

        # Boutons du menu
        center_x = config.SCREEN_WIDTH // 2
        center_y = config.SCREEN_HEIGHT // 2

        self.play_button_rect = pygame.Rect(center_x - 100, center_y + 100, 200, 50)
        self.speed_slow_rect = pygame.Rect(center_x - 210, center_y - 50, 130, 60)
        self.speed_normal_rect = pygame.Rect(center_x - 65, center_y - 50, 130, 60)
        self.speed_fast_rect = pygame.Rect(center_x + 80, center_y - 50, 130, 60)
        self.restart_button_rect = pygame.Rect(center_x - 100, center_y + 50, 200, 50)

    def draw_overlay(self, alpha=160):
        """Dessiner fond semi-transparent"""
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        overlay.set_alpha(alpha)
        overlay.fill("black")
        self.screen.blit(overlay, (0, 0))

    def draw_main_menu(self):
        """Dessiner le menu principal"""
        self.draw_overlay()

        # Titre
        title_text = self.font.render("THE EEL", True, "white")
        title_rect = title_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 150))
        self.screen.blit(title_text, title_rect)

        # Label vitesse
        speed_label = self.font.render("Speed:", True, "white")
        speed_label_rect = speed_label.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(speed_label, speed_label_rect)

        # Boutons de vitesse
        self._draw_speed_buttons()

        # Bouton PLAY
        self._draw_button(self.play_button_rect, "PLAY", "darkgreen", "white", 3)

    def draw_game_over(self, final_score):
        """Dessiner l'écran de game over"""
        self.draw_overlay(128)

        center_x = config.SCREEN_WIDTH // 2
        center_y = config.SCREEN_HEIGHT // 2

        # Texte Game Over
        game_over_text = self.font.render("GAME OVER", True, "white")
        game_over_rect = game_over_text.get_rect(center=(center_x, center_y - 50))
        self.screen.blit(game_over_text, game_over_rect)

        # Score final
        score_text = self.font.render(f"Final Score: {final_score}", True, "white")
        score_rect = score_text.get_rect(center=(center_x, center_y - 10))
        self.screen.blit(score_text, score_rect)

        # Bouton Restart
        self._draw_button(self.restart_button_rect, "RESTART", "darkgreen", "white", 2)

    def _draw_speed_buttons(self):
        """Dessiner les boutons de sélection de vitesse"""
        speeds = [
            (self.speed_slow_rect, "SLOW", config.SPEED_SLOW),
            (self.speed_normal_rect, "NORMAL", config.SPEED_NORMAL),
            (self.speed_fast_rect, "FAST", config.SPEED_FAST)
        ]

        for rect, text, speed in speeds:
            is_selected = speed == self.selected_speed
            bg_color = "green" if is_selected else "darkgray"
            border_color = "white" if is_selected else "gray"

            self._draw_button(rect, text, bg_color, border_color, 2)

    def _draw_button(self, rect, text, bg_color, border_color, border_width):
        """Dessiner un bouton générique"""
        pygame.draw.rect(self.screen, bg_color, rect)
        pygame.draw.rect(self.screen, border_color, rect, border_width)

        button_text = self.font.render(text, True, "white")
        text_rect = button_text.get_rect(center=rect.center)
        self.screen.blit(button_text, text_rect)

    def handle_click(self, pos):
        """Gérer les clics dans le menu principal"""
        if self.speed_slow_rect.collidepoint(pos):
            self.selected_speed = config.SPEED_SLOW
            return "speed_changed"
        elif self.speed_normal_rect.collidepoint(pos):
            self.selected_speed = config.SPEED_NORMAL
            return "speed_changed"
        elif self.speed_fast_rect.collidepoint(pos):
            self.selected_speed = config.SPEED_FAST
            return "speed_changed"
        elif self.play_button_rect.collidepoint(pos):
            return "play"
        return None

    def handle_game_over_click(self, pos):
        """Gérer les clics dans l'écran game over"""
        if self.restart_button_rect.collidepoint(pos):
            return "restart"
        return None

    def get_selected_speed(self):
        """Obtenir la vitesse sélectionnée"""
        return self.selected_speed