import pygame
from . import config
from .eel import Eel
from .food import Food
from .grid import Grid
from .menu import Menu
from .game_state import GameStateManager


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

        # Gestionnaires
        self.state_manager = GameStateManager()
        self.menu = Menu(self.screen, self.font)

        # Composants du jeu
        self._init_game_components()

    def _init_game_components(self):
        """Initialiser les composants de jeu"""
        self.eel = Eel(5, 5)
        self.food = Food()
        self.grid = Grid(self.center)
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
                self._handle_mouse_click(event.pos)

        # Gestion des entrées clavier pour l'anguille
        if self.state_manager.is_waiting_start or self.state_manager.is_playing:
            keys = pygame.key.get_pressed()
            self._handle_keyboard_input(keys)

    def update(self):
        """Mettre à jour la logique du jeu"""
        if not self.state_manager.should_update_game():
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
            self.state_manager.game_over()
            return

        # Collision avec soi-même
        if self.eel.check_self_collision():
            print("Game Over: Collision avec soi-même")
            self.state_manager.game_over()
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

        # Toujours dessiner le jeu en arrière-plan
        self._draw_game_elements()

        # Dessiner les overlays selon l'état
        if self.state_manager.is_menu:
            self.menu.draw_main_menu()
        elif self.state_manager.is_game_over:
            final_score = self._calculate_final_score()
            self.menu.draw_game_over(final_score)
        else:
            self._draw_score()

        pygame.display.flip()

    def _draw_game_elements(self):
        """Dessiner les éléments de jeu (grille, anguille, nourriture)"""
        self.grid.draw(self.screen, config.CELL_SIZE)
        grid_bounds = self.grid.get_bounds()
        self.food.draw(self.screen, grid_bounds)
        self.eel.draw(self.screen, grid_bounds)

    def _draw_score(self):
        """Dessiner le score en haut à gauche"""
        if self.eel.segments_added < self.eel.initial_segments_to_add:
            score = 0
        else:
            score = len(self.eel.body) - self.eel.initial_segments_to_add
        score_text = self.font.render(f"Score: {score}", True, "white")
        self.screen.blit(score_text, (20, 20))

    def _calculate_final_score(self):
        """Calculer le score final"""
        if self.eel.segments_added >= self.eel.initial_segments_to_add:
            return len(self.eel.body) - self.eel.initial_segments_to_add
        return 0

    def _handle_mouse_click(self, pos):
        """Gérer les clics de souris selon l'état"""
        if self.state_manager.is_menu:
            action = self.menu.handle_click(pos)
            if action == "play":
                self._start_new_game()
        elif self.state_manager.is_game_over:
            action = self.menu.handle_game_over_click(pos)
            if action == "restart":
                self._restart_game()

    def _handle_keyboard_input(self, keys):
        """Gérer les entrées clavier"""
        directions = {
            (pygame.K_z, pygame.K_UP): pygame.Vector2(0, -1),
            (pygame.K_s, pygame.K_DOWN): pygame.Vector2(0, 1),
            (pygame.K_q, pygame.K_LEFT): pygame.Vector2(-1, 0),
            (pygame.K_d, pygame.K_RIGHT): pygame.Vector2(1, 0)
        }

        for key_pair, direction in directions.items():
            if any(keys[key] for key in key_pair):
                if self.state_manager.is_waiting_start:
                    # Ne pas démarrer vers la gauche
                    if direction.x == -1:
                        continue
                    self.state_manager.begin_playing()
                    self.eel.start_movement(direction)
                elif self.state_manager.is_playing:
                    self.eel.set_pending_direction(direction)
                break

    def _start_new_game(self):
        """Démarrer une nouvelle partie"""
        selected_speed = self.menu.get_selected_speed()
        config.MOVE_INTERVAL = selected_speed
        self.state_manager.start_game()
        self._init_game_components()

    def _restart_game(self):
        """Redémarrer le jeu"""
        self.state_manager.restart()
        self._init_game_components()

