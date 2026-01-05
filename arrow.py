from dataclasses import dataclass, field
import pygame


@dataclass
class Arrow:
    position: pygame.Vector2
    velocity: pygame.Vector2
    shape: list = field(
        default_factory=lambda: [[0, 0], [300, 100], [0, 200], [50, 100], [0, 0]]
    )

    def draw(self, screen):
        # Draw an arrow
        pygame.draw.polygon(screen, "black", self.shape)

    def update(self):
        # Move the arrow
        self.shape = [(x + 1, y + 0) for x, y in self.shape]
