from dataclasses import dataclass, field
from arrow import Arrow
import random
import pygame


@dataclass
class BoidSystem:
    num_arrows: int
    screen: pygame.Surface
    arrows: list[Arrow] = field(default_factory=lambda: [])

    def __post_init__(self):
        for _ in range(self.num_arrows):
            position = pygame.Vector2(
                random.uniform(0, self.screen.get_width()),
                random.uniform(0, self.screen.get_height()),
            )

            arrow = Arrow(self.screen, position, scale=0.2)
            self.arrows.append(arrow)

    def update(self):
        # Update Grouping and distancing of entity
        self.personalSpace()
        self.debugVisuals()

    def personalSpace(self) -> None:
        for arrow in self.arrows:
            ...

    def debugVisuals(self):
        # Draw a transparent circle around the first arrow to represent its personal space
        first_arrow = self.arrows[0]
        personal_space_radius = 100
        transparent_surface = pygame.Surface(
            (self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA
        )
        pygame.draw.circle(
            transparent_surface,
            (0, 0, 255, 50),  # RGBA color with alpha for transparency
            (int(first_arrow.position.x), int(first_arrow.position.y)),
            personal_space_radius,
        )
        self.screen.blit(transparent_surface, (0, 0))
