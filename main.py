import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from boid import BoidSystem
from slider import SliderWithLabel

# pygame setup
pygame.init()
screen: pygame.Surface = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

boidSystem = BoidSystem(50, screen)

# Create sliders
alignment_slider = SliderWithLabel(
    screen, "alignment", 50, 600, 200, 20, 0, 5, 0.1, label_font_size=20
)
cohesion_slider = SliderWithLabel(
    screen, "cohesion", 300, 600, 200, 20, 0, 5, 0.1, label_font_size=20
)
separation_slider = SliderWithLabel(
    screen, "separation", 550, 600, 200, 20, 0, 5, 0.1, label_font_size=20
)

while running:

    events = pygame.event.get()

    for event in events:

        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    # Get mouse position in order to let the arrows target it
    mouse_pos: tuple[int, int] = pygame.mouse.get_pos()

    boidSystem.update(mouse_pos)

    pygame_widgets.update(events)

    # Update slider lables
    alignment_slider.update_label()
    cohesion_slider.update_label()
    separation_slider.update_label()

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
