import pygame
from arrow import Arrow

# pygame setup
pygame.init()
screen: pygame.Surface = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# Create multiple arrows
arrows = [
    Arrow(
        screen,
        position=pygame.Vector2(
            screen.get_width() / 2 + i * 30, screen.get_height() / 2
        ),
        scale=0.1,
    )
    for i in range(10)
]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    mouse_pos: tuple[int, int] = pygame.mouse.get_pos()
    pygame.draw.circle(screen, "black", mouse_pos, 10)

    for arrow in arrows:
        arrow.draw()
        arrow.drawPosition()
        arrow.update(mouse_pos)

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
