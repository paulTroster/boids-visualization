from dataclasses import dataclass, field
from typing import ClassVar
import pygame


@dataclass
class Arrow:

    screen: pygame.Surface
    position: pygame.Vector2
    velocity: pygame.Vector2
    acceleration: pygame.Vector2
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

    def draw(self):
        # Draw an arrow
        pygame.draw.polygon(self.screen, "black", self.shape)

    def drawPosition(self):
        # Draw the position of the Arrow for debugging
        pygame.draw.circle(self.screen, "red", self.position, 20 * self.scale)

    def update(self, targetPos: tuple[int, int]):

        acc: pygame.Vector2 = self.calculateAcceleration(targetPos)
        self.velocity += pygame.Vector2.normalize(acc) * 0.8
        self.position += self.velocity

        self.checkEdges()
        self.recalculateShape()

    def calculateAcceleration(self, targetPos) -> pygame.Vector2:
        return pygame.Vector2(
            targetPos[0] - self.position.x, targetPos[1] - self.position.y
        )

    def checkEdges(self, hardEdges: bool = False):
        """
        Check the edges and decide whether arrows bounce on edges or spawn on the other side
        """
        if hardEdges == False:
            if self.position.x > self.screen.get_width():
                self.position.x = 0

            if self.position.x < 0:
                self.position.x = self.screen.get_width()

            if self.position.y > self.screen.get_height() or self.position.y < 0:
                self.position.y = 0

            if self.position.y < 0:
                self.position.y = self.screen.get_height()
        else:
            if self.position.x > self.screen.get_width() or self.position.x < 0:
                self.velocity.x = self.velocity.x * -1

            if self.position.y > self.screen.get_height() or self.position.y < 0:
                self.velocity.y = self.velocity.y * -1
