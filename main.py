import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from boid import BoidSystem

# pygame setup
pygame.init()
screen: pygame.Surface = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

boidSystem = BoidSystem(50, screen)

slider = Slider(screen, 100, 100, 800, 40, min=0, max=99, step=1)
output = TextBox(screen, 475, 200, 100, 50, fontSize=30)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    pygame_widgets.update(screen)

    # Get mouse position in order to let the arrows target it
    mouse_pos: tuple[int, int] = pygame.mouse.get_pos()

    boidSystem.update(mouse_pos)

    output.setText(str(slider.getValue()))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        running = False

    # if pygame.mouse.get_pressed()[0] == True:
    #     boidSystem.applyForceToAll(pygame.Vector2(0, 0.1))  # Add gravitation

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
