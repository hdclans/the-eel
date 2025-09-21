import pygame
from . import config
from .eel import Eel
from .food import Food
from .grid import Grid


class Game:
    """Classe principale"""

    def __init__(self):
        pygame.init()

        # Configuration de la fenêtre
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("The Eel")
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0

        # Police pour le score
        self.font = pygame.font.Font(None, 36)

        # Centre de l'écran
        self.center = pygame.Vector2(
            self.screen.get_width() / 2,
            self.screen.get_height() / 2
        )

        # Composants du jeu
        self.eel = Eel(5, 5)
        self.food = Food()
        self.grid = Grid(self.center)

        # Délai de démarrage
        self.start_delay = 2.0
        self.start_timer = 0.0
        self.game_started = False

        # État du jeu
        self.game_over = False
        self.restart_button_rect = pygame.Rect(config.SCREEN_WIDTH // 2 - 100, config.SCREEN_HEIGHT // 2 + 50, 200, 50)

        # Initialiser la nourriture en évitant l'anguille
        self.food.generate([self.eel.get_head_position()])

    def run(self):
        while self.running:
            self.handle_events()   # Gestion des événements (clavier, souris, fermeture fenêtre)
            self.update()          # Logique du jeu (mouvements, collisions...)
            self.draw()            # Rendu graphique

            # Calcul du delta time (temps entre deux frames)
            self.dt = self.clock.tick(config.FPS) / 1000

        pygame.quit()

    def handle_events(self):
        """Gérer les événements pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over and self.restart_button_rect.collidepoint(event.pos):
                    self.restart_game()

        # Gestion des entrées clavier pour l'anguille
        if not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_z] or keys[pygame.K_UP]:
                if not self.game_started:
                    self.game_started = True
                    self.eel.start_movement(pygame.Vector2(0, -1))  # Démarrer vers le haut
                else:
                    self.eel.set_pending_direction(pygame.Vector2(0, -1))
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                if not self.game_started:
                    self.game_started = True
                    self.eel.start_movement(pygame.Vector2(0, 1))   # Démarrer vers le bas
                else:
                    self.eel.set_pending_direction(pygame.Vector2(0, 1))
            elif keys[pygame.K_q] or keys[pygame.K_LEFT]:
                if not self.game_started:
                    pass
                else:
                    self.eel.set_pending_direction(pygame.Vector2(-1, 0))
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                if not self.game_started:
                    self.game_started = True
                    self.eel.start_movement(pygame.Vector2(1, 0))   # Démarrer vers la droite
                else:
                    self.eel.set_pending_direction(pygame.Vector2(1, 0))

    def update(self):
        """Mettre à jour la logique du jeu"""
        # attendre le premier clic de flèche
        if not self.game_started or self.game_over:
            return

        # Mise à jour de l'anguille
        self.eel.update_movement(self.dt)

        # Vérifier les collisions
        self._check_collisions()

    def _check_collisions(self):
        """Vérifier toutes les collisions"""
        # Collision avec les limites
        if self.eel.is_out_of_bounds():
            print(f"Game Over: Sortie de grille")
            self.game_over = True
            return

        # Collision avec soi-même
        if self.eel.check_self_collision():
            print("Game Over: Collision avec soi-même")
            self.game_over = True
            return

        # Collision avec la nourriture
        head_pos = self.eel.get_head_position()
        food_pos = self.food.get_position()

        if head_pos == food_pos:
            self.eel.add_segment()
            # Régénérer la nourriture en évitant l'anguille'
            avoid_positions = [head_pos] + [tuple(map(int, segment)) for segment in self.eel.body]
            self.food.generate(avoid_positions)

    def draw(self):
        """Dessiner tous les éléments du jeu"""
        self.screen.fill(config.BG_COLOR)

        self.grid.draw(self.screen, config.CELL_SIZE)

        # Obtenir les limites de la grille
        grid_bounds = self.grid.get_bounds()

        self.food.draw(self.screen, grid_bounds)

        self.eel.draw(self.screen, grid_bounds)

        self._draw_score()

        if self.game_over:
            self._draw_game_over()

        pygame.display.flip()

    def _draw_score(self):
        """Dessiner le score en haut à gauche"""
        if self.eel.segments_added < self.eel.initial_segments_to_add:
            score = 0
        else:
            score = len(self.eel.body) - self.eel.initial_segments_to_add
        score_text = self.font.render(f"Score: {score}", True, "white")
        self.screen.blit(score_text, (20, 20))

    def _draw_game_over(self):
        """Dessiner l'écran de game over avec bouton restart"""
        # Fond semi-transparent
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill("black")
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.font.render("GAME OVER", True, "white")
        game_over_rect = game_over_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, game_over_rect)

        # Score final
        final_score = len(self.eel.body) - self.eel.initial_segments_to_add if self.eel.segments_added >= self.eel.initial_segments_to_add else 0
        score_text = self.font.render(f"Final Score: {final_score}", True, "white")
        score_rect = score_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 10))
        self.screen.blit(score_text, score_rect)

        # Bouton Restart
        pygame.draw.rect(self.screen, "darkgreen", self.restart_button_rect)
        pygame.draw.rect(self.screen, "white", self.restart_button_rect, 2)
        restart_text = self.font.render("RESTART", True, "white")
        restart_rect = restart_text.get_rect(center=self.restart_button_rect.center)
        self.screen.blit(restart_text, restart_rect)

    def restart_game(self):
        """Redémarrer le jeu"""
        self.game_over = False
        self.game_started = False
        self.eel = Eel(5, 5)
        self.food = Food()
        self.food.generate([self.eel.get_head_position()])
