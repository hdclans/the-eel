import pygame
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
                self.running = False

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

        # Dessiner l'anguille à sa position interpolée
        pixel_pos = self.get_pixel_position()
        pygame.draw.circle(self.screen, config.PLAYER_COLOR, pixel_pos, config.PLAYER_RADIUS) # Dessine l'anguille
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
