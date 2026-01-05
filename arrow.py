from dataclasses import dataclass, field
from typing import ClassVar
import pygame


@dataclass
class Arrow:
    position: pygame.Vector2
    velocity: pygame.Vector2
    shape: list = field(init=False)
    scale: float = 1

    BASE_SHAPE: ClassVar[list] = [[0, 0], [300, 100], [0, 200], [50, 100], [0, 0]]
    ARROW_OFFSET: ClassVar[pygame.Vector2] = pygame.Vector2(
        150, 100
    )  # half of the width and height of the shape

    def __post_init__(self):
        self.recalculateShape()

    def recalculateShape(self):
        self.shape = [
            (
                ((x * self.scale) + self.position.x - self.ARROW_OFFSET.x * self.scale),
                ((y * self.scale) + self.position.y - self.ARROW_OFFSET.y * self.scale),
            )
            for x, y in self.BASE_SHAPE
        ]

    def draw(self, screen):
        # Draw an arrow
        pygame.draw.polygon(screen, "black", self.shape)

    def drawPosition(self, screen):
        # Draw the position of the Arrow for debugging
        pygame.draw.circle(screen, "red", self.position, 20 * self.scale)

    def update(self):
        # Move the arrow
        self.shape = [(x + self.velocity.x, y + self.velocity.y) for x, y in self.shape]
