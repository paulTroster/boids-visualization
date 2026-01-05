import pygame
from arrow import Arrow

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# Create an arrow
arrow = Arrow(player_pos, pygame.Vector2(5, 5), 0.1)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    arrow.draw(screen)
    arrow.drawPosition(screen)
    arrow.update()

    if arrow.position.x > screen.get_width() or arrow.position.x < 0:
        arrow.velocity.x = arrow.velocity.x * -1

    if arrow.position.y > screen.get_height() or arrow.position.y < 0:
        arrow.velocity.y = arrow.velocity.y * -1

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
