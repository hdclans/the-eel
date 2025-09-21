import pygame
import random
from . import config

class Game:
    def __init__(self):
        pygame.init()
        # Création de la fenêtre principale avec largeur et hauteur définies dans config
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("The eel")  # Titre de la fenêtre
        self.clock = pygame.time.Clock()       # Horloge pour contrôler le framerate
        self.running = True                    # Booléen pour garder la boucle principale active
        self.dt = 0                            # Delta time = temps écoulé entre deux frames

        # Centre de l’écran
        self.center = pygame.Vector2(
            self.screen.get_width() / 2, 
            self.screen.get_height() / 2
        )

        # Position initiale (pour référence)
        self.player_pos_init = pygame.Vector2(self.screen.get_width() / 2 - 164, self.screen.get_height() / 2 + 1)

        # Position en coordonnées de grille
        self.grid_x = 5
        self.grid_y = 5
        self.target_grid_x = 5
        self.target_grid_y = 5
        self.auto_direction = pygame.Vector2(1, 0)
        self.move_timer = 0
        self.pending_direction = None
        self.first_move = True  # Pour gérer le premier mouvement

        # Délai de démarrage
        self.start_delay = 2.0
        self.start_timer = 0.0
        self.game_started = False

        # nourriture
        self.food_x = 0
        self.food_y = 0
        self.generate_food()

        # Corps de l'anguille (segments qui suivent)
        self.body = []  # Liste des positions des segments du corps
        self.body_history = []  # Historique des positions pour que les segments suivent

    def run(self):
        while self.running:
            self.handle_events()   # Gestion des événements (clavier, souris, fermeture fenêtre)
            self.update()          # Logique du jeu (mouvements, collisions...)
            self.draw()            # Rendu graphique

            # Calcul du delta time (temps entre deux frames)
            self.dt = self.clock.tick(config.FPS) / 1000

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        # Gestion du délai de démarrage
        if not self.game_started:
            self.start_timer += self.dt
            if self.start_timer >= self.start_delay:
                self.game_started = True
                # Réinitialiser le timer de mouvement pour démarrer proprement
                self.move_timer = 0
            # Pendant le délai, rester à la position initiale (5,5)
            self.grid_x = 5
            self.grid_y = 5
            return

        # Mise à jour du timer pour les changements de direction
        self.move_timer += self.dt

        # Contrôle de direction avec les touches (stockage en attente)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z] or keys[pygame.K_UP]:
            self.pending_direction = pygame.Vector2(0, -1)
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.pending_direction = pygame.Vector2(0, 1)
        elif keys[pygame.K_q] or keys[pygame.K_LEFT]:
            self.pending_direction = pygame.Vector2(-1, 0)
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.pending_direction = pygame.Vector2(1, 0)

        # Changement de direction et mouvement synchronisés toutes les MOVE_INTERVAL secondes
        if self.move_timer >= config.MOVE_INTERVAL:
            self.move_timer = 0

            # Appliquer le changement de direction si valide
            if self.pending_direction and self.is_valid_direction_change(self.pending_direction):
                self.auto_direction = self.pending_direction
                self.pending_direction = None

            # Pour le premier mouvement, démarrer de la position initiale
            if self.first_move:
                self.first_move = False
                # Définir la première cible
                self.target_grid_x = 5 + self.auto_direction.x
                self.target_grid_y = 5 + self.auto_direction.y
            else:
                # Déplacement normal d'une case
                new_target_x = self.target_grid_x + self.auto_direction.x
                new_target_y = self.target_grid_y + self.auto_direction.y
                self.target_grid_x = new_target_x
                self.target_grid_y = new_target_y

            # Vérifier les limites de la grille
            if not (0 <= self.target_grid_x < 11 and 0 <= self.target_grid_y < 11):
                print(f"Game Over: Sortie de grille - Position cible: ({self.target_grid_x}, {self.target_grid_y})")
                self.running = False

        # Ajouter la position actuelle à l'historique
        self.body_history.append((self.grid_x, self.grid_y))

        # Vérifier collision avec la nourriture
        current_grid_x = int(round(self.grid_x))
        current_grid_y = int(round(self.grid_y))
        if current_grid_x == self.food_x and current_grid_y == self.food_y:
            # Ajouter un nouveau segment au corps à une position éloignée
            positions_per_cell = int(config.MOVE_INTERVAL * config.FPS)
            new_segment_index = len(self.body) * positions_per_cell + positions_per_cell
            if len(self.body_history) > new_segment_index:
                self.body.append((self.body_history[-new_segment_index][0], self.body_history[-new_segment_index][1]))
            else:
                # Si pas assez d'historique, placer le segment hors de portée temporairement
                self.body.append((-10, -10))
            self.generate_food()

        # Vérifier collision avec le corps de l'anguille seulement quand la tête est proche d'une position entière
        if abs(self.grid_x - round(self.grid_x)) < 0.1 and abs(self.grid_y - round(self.grid_y)) < 0.1:
            for i, segment in enumerate(self.body):
                segment_grid_x = int(round(segment[0]))
                segment_grid_y = int(round(segment[1]))
                # Ignorer les segments hors de la grille (segments temporaires)
                if (0 <= segment_grid_x < 11 and 0 <= segment_grid_y < 11 and
                    current_grid_x == segment_grid_x and current_grid_y == segment_grid_y):
                    self.running = False

        # Mettre à jour les positions des segments du corps
        for i in range(len(self.body)):
            positions_per_cell = int(config.MOVE_INTERVAL * config.FPS)
            history_index = len(self.body_history) - 1 - (i + 1) * positions_per_cell
            if history_index >= 0:
                self.body[i] = self.body_history[history_index]

        # Limiter la taille de l'historique pour éviter une croissance infinie
        positions_per_cell = int(config.MOVE_INTERVAL * config.FPS)
        max_history = len(self.body) * positions_per_cell + 100
        if len(self.body_history) > max_history:
            self.body_history = self.body_history[-max_history:]

        # Interpolation fluide vers la position cible
        progress = self.move_timer / config.MOVE_INTERVAL
        progress = min(progress, 1.0)

        if self.first_move:
            # Avant le premier mouvement, rester à la position initiale
            self.grid_x = 5
            self.grid_y = 5
        else:
            # Calculer la position entre position actuelle et cible
            start_x = self.target_grid_x - self.auto_direction.x
            start_y = self.target_grid_y - self.auto_direction.y

            self.grid_x = start_x + (self.target_grid_x - start_x) * progress
            self.grid_y = start_y + (self.target_grid_y - start_y) * progress
                
    # Empêcher les demi-tours
    def is_valid_direction_change(self, new_direction):
        return new_direction != -self.auto_direction

    def generate_food(self):
        # Générer une position aléatoire pour la nourriture
        self.food_x = random.randint(0, 10)
        self.food_y = random.randint(0, 10)

        # S'assurer que la nourriture n'apparaît pas sur le joueur
        current_player_x = int(round(self.grid_x))
        current_player_y = int(round(self.grid_y))

        if self.food_x == current_player_x and self.food_y == current_player_y:
            self.generate_food()

    def get_pixel_position(self):
        # Convertir position grille en pixels
        if hasattr(self, 'grid_bounds'):
            pixel_x = self.grid_bounds.left + (self.grid_x * config.CELL_SIZE) + (config.CELL_SIZE // 2)
            pixel_y = self.grid_bounds.top + (self.grid_y * config.CELL_SIZE) + (config.CELL_SIZE // 2)
            return pygame.Vector2(pixel_x, pixel_y)
        return pygame.Vector2(self.grid_x * config.CELL_SIZE, self.grid_y * config.CELL_SIZE)

    def draw(self):
        self.screen.fill(config.BG_COLOR)  # Efface l'écran avec la couleur de fond
        self.grid(config.CELL_SIZE)        # Dessine une grille centrée

        # Dessiner la nourriture
        if hasattr(self, 'grid_bounds'):
            food_pixel_x = self.grid_bounds.left + (self.food_x * config.CELL_SIZE) + (config.CELL_SIZE // 2)
            food_pixel_y = self.grid_bounds.top + (self.food_y * config.CELL_SIZE) + (config.CELL_SIZE // 2)
            pygame.draw.circle(self.screen, "red", (food_pixel_x, food_pixel_y), 8)  # Petit cercle rouge

        # Dessiner les segments du corps de l'anguille
        if hasattr(self, 'grid_bounds'):
            for segment_pos in self.body:
                segment_pixel_x = self.grid_bounds.left + (segment_pos[0] * config.CELL_SIZE) + (config.CELL_SIZE // 2)
                segment_pixel_y = self.grid_bounds.top + (segment_pos[1] * config.CELL_SIZE) + (config.CELL_SIZE // 2)
                pygame.draw.circle(self.screen, config.PLAYER_COLOR, (segment_pixel_x, segment_pixel_y), config.PLAYER_RADIUS)

        # Dessiner la tête de l'anguille à sa position interpolée
        pixel_pos = self.get_pixel_position()
        pygame.draw.circle(self.screen, config.PLAYER_COLOR, pixel_pos, config.PLAYER_RADIUS) # Dessine la tête
        pygame.display.flip()              # Met à jour l'affichage

    def grid(self, cell_size):
        rect_width = 605
        rect_height = 605

        # Définition d'un rectangle centré
        rect = pygame.Rect(0, 0, rect_width - 1, rect_height - 1)
        rect.center = self.center

        # Stockage des limites de la grille pour les collisions
        self.grid_bounds = rect

        # Lignes verticales
        for x in range(rect.left, rect.right + 1, cell_size):
            pygame.draw.line(
                self.screen, "darkgrey",
                (x, rect.top), (x, rect.bottom), 1
            )

        # Lignes horizontales
        for y in range(rect.top, rect.bottom  + 1, cell_size):
            pygame.draw.line(
                self.screen, "darkgrey",
                (rect.left, y), (rect.right, y), 1
            )

        # Bord rouge
        pygame.draw.rect(self.screen, "red", rect, 3)
