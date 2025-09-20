import pygame
from . import config

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("The eel")
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0

        self.player_pos = pygame.Vector2(
            self.screen.get_width() / 2, 
            self.screen.get_height() / 2
        )

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            self.dt = self.clock.tick(config.FPS) / 1000

        pygame.quit()

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
        self.screen.fill(config.BG_COLOR)
        pygame.draw.circle(self.screen, config.PLAYER_COLOR, self.player_pos, config.PLAYER_RADIUS)
        pygame.display.flip()
