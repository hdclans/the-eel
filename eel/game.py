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

        self.player_pos = pygame.Vector2(self.screen.get_width() / 2 - 164, self.screen.get_height() / 2 + 1)

    def run(self):
        while self.running:
            self.handle_events()   # Gestion des événements (clavier, souris, fermeture fenêtre)
            self.update()          # Logique du jeu (mouvements, collisions...)
            self.draw()            # Rendu graphique

            # Calcul du delta time (temps entre deux frames)
            self.dt = self.clock.tick(config.FPS) / 1000

        pygame.quit()              # Quitter pygame

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z] or keys[pygame.K_UP]:
            self.player_pos.y -= config.PLAYER_SPEED * self.dt

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.player_pos.y += config.PLAYER_SPEED * self.dt

        if keys[pygame.K_q] or keys[pygame.K_LEFT]:
            self.player_pos.x -= config.PLAYER_SPEED * self.dt

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player_pos.x += config.PLAYER_SPEED * self.dt

    def draw(self):
        self.screen.fill(config.BG_COLOR)  # Efface l’écran avec la couleur de fond
        self.grid(config.CELL_SIZE)        # Dessine une grille centrée        
        pygame.draw.circle(self.screen, config.PLAYER_COLOR, self.player_pos, config.PLAYER_RADIUS) # Dessine l'anguille
        pygame.display.flip()              # Met à jour l’affichage

    def grid(self, cell_size):
        rect_width = 605
        rect_height = 605

        # Définition d’un rectangle centré
        rect = pygame.Rect(0, 0, rect_width, rect_height)
        rect.center = self.center

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
