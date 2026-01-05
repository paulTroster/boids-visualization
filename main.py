import pygame
from boid import BoidSystem
from arrow import Arrow

# pygame setup
pygame.init()
screen: pygame.Surface = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

boidSystem = BoidSystem(10, screen)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    mouse_pos: tuple[int, int] = pygame.mouse.get_pos()
    pygame.draw.circle(screen, "black", mouse_pos, 10)

    for arrow in boidSystem.arrows:
        arrow.draw()
        arrow.drawPosition()
        arrow.update(mouse_pos)

    boidSystem.update()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        running = False

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
