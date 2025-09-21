import pygame
from . import config
from .snake import Snake
from .food import Food
from .grid import Grid


class Game:
    """Classe principale du jeu Snake/Eel"""

    def __init__(self):
        pygame.init()

        # Configuration de la fenêtre
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("The Eel")
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0

        # Centre de l'écran
        self.center = pygame.Vector2(
            self.screen.get_width() / 2,
            self.screen.get_height() / 2
        )

        # Composants du jeu
        self.snake = Snake(5, 5)
        self.food = Food()
        self.grid = Grid(self.center)

        # Délai de démarrage
        self.start_delay = 2.0
        self.start_timer = 0.0
        self.game_started = False

        # Initialiser la nourriture en évitant l'anguille
        self.food.generate([self.snake.get_head_position()])

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

        # Gestion des entrées clavier pour l'anguille
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z] or keys[pygame.K_UP]:
            self.snake.set_pending_direction(pygame.Vector2(0, -1))
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.snake.set_pending_direction(pygame.Vector2(0, 1))
        elif keys[pygame.K_q] or keys[pygame.K_LEFT]:
            self.snake.set_pending_direction(pygame.Vector2(-1, 0))
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.snake.set_pending_direction(pygame.Vector2(1, 0))

    def update(self):
        """Mettre à jour la logique du jeu"""
        # Gestion du délai de démarrage
        if not self.game_started:
            self.start_timer += self.dt
            if self.start_timer >= self.start_delay:
                self.game_started = True
            return

        # Mise à jour de l'anguille
        self.snake.update_movement(self.dt)

        # Vérifier les collisions
        self._check_collisions()

    def _check_collisions(self):
        """Vérifier toutes les collisions"""
        # Collision avec les limites
        if self.snake.is_out_of_bounds():
            print(f"Game Over: Sortie de grille")
            self.running = False
            return

        # Collision avec soi-même
        if self.snake.check_self_collision():
            print("Game Over: Collision avec soi-même")
            self.running = False
            return

        # Collision avec la nourriture
        head_pos = self.snake.get_head_position()
        food_pos = self.food.get_position()

        if head_pos == food_pos:
            self.snake.add_segment()
            # Régénérer la nourriture en évitant l'anguille'
            avoid_positions = [head_pos] + [tuple(map(int, segment)) for segment in self.snake.body]
            self.food.generate(avoid_positions)

    def draw(self):
        """Dessiner tous les éléments du jeu"""
        self.screen.fill(config.BG_COLOR)

        # Dessiner la grille
        self.grid.draw(self.screen, config.CELL_SIZE)

        # Obtenir les limites de la grille
        grid_bounds = self.grid.get_bounds()

        # Dessiner la nourriture
        self.food.draw(self.screen, grid_bounds)

        # Dessiner l'anguille'
        self.snake.draw(self.screen, grid_bounds)

        pygame.display.flip()
