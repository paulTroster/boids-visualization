import pygame
import random
import math
from boid import BoidSystem
from arrow import Arrow

# pygame setup
pygame.init()
screen: pygame.Surface = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

boidSystem = BoidSystem(15, screen)

# Wind variables
wind_change_timer = 0
wind_change_interval = random.uniform(3, 6)
current_wind_direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
target_wind_direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
current_wind_strength = random.uniform(0.05, 0.2)
target_wind_strength = random.uniform(0.05, 0.2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    # Get mouse position in order to let the arrows target it
    mouse_pos: tuple[int, int] = pygame.mouse.get_pos()

    boidSystem.update(mouse_pos)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        running = False

    if pygame.mouse.get_pressed()[0] == True:
        boidSystem.applyForceToAll(pygame.Vector2(0, 0.1))  # Add gravitation

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
