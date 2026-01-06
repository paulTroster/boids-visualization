from dataclasses import dataclass, field
from typing import ClassVar
from math import atan2, cos, sin
import pygame


@dataclass
class Arrow:

    screen: pygame.Surface
    position: pygame.Vector2
    max_speed: float = 15
    velocity: pygame.Vector2 = field(default_factory=lambda: pygame.Vector2(0, 0))
    acceleration: pygame.Vector2 = field(default_factory=lambda: pygame.Vector2(0, 0))
    shape: list = field(init=False)
    scale: float = 1

    BASE_SHAPE: ClassVar[list] = [
        [-150, -100],
        [150, 0],
        [-150, 100],
        [-100, 0],
        [-150, -100],
    ]

    def __post_init__(self):
        self.recalculateShape()

    def draw(self):
        # Draw an arrow
        pygame.draw.polygon(self.screen, "black", self.shape)

    def drawPosition(self):
        # Draw the position of the Arrow for debugging
        pygame.draw.circle(self.screen, "red", self.position, 20 * self.scale)

    def update(self, targetPos: tuple[int, int], targetActive=False):
        if targetActive:
            # Set the Velocity towards the target
            acc: pygame.Vector2 = self.calculateAcceleration(targetPos)
            self.velocity += pygame.Vector2.clamp_magnitude(acc, 0.8)
            
            # Apply accumulated forces (like avoidance)
            self.velocity += self.acceleration
            
            self.velocity = pygame.Vector2.clamp_magnitude(
                self.velocity, self.max_speed
            )
            self.position += self.velocity
        else:
            self.velocity += self.acceleration
            self.position += self.velocity

        # Reset acceleration for next frame
        self.acceleration = pygame.Vector2(0, 0)

        self.rotatePoly()
        self.checkEdges(hardEdges=False)

    def applyForce(self, force: pygame.Vector2):
        self.acceleration += force

    def recalculateShape(self):
        self.shape = [
            (((x * self.scale) + self.position.x), ((y * self.scale) + self.position.y))
            for x, y in self.BASE_SHAPE
        ]

    def calculateAcceleration(self, targetPos) -> pygame.Vector2:
        return pygame.Vector2(
            targetPos[0] - self.position.x, targetPos[1] - self.position.y
        )

    def rotatePoly(self):
        angle = self.velocityToRotation()
        self.shape = []
        for x, y in self.BASE_SHAPE:
            px, py = self.transformPoint(
                pygame.Vector2(x * self.scale, y * self.scale), angle
            )
            self.shape.append((px + self.position.x, py + self.position.y))

    def transformPoint(
        self, point: pygame.Vector2, angle: float
    ) -> tuple[float, float]:
        x, y = point
        cos_a = cos(angle)
        sin_a = sin(angle)
        return (x * cos_a - y * sin_a, x * sin_a + y * cos_a)

    def velocityToRotation(self) -> float:
        return atan2(self.velocity.y, self.velocity.x)

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

            if self.position.x > self.screen.get_width():
                self.position.x = self.screen.get_width()

            if self.position.x < 0:
                self.position.x = 0

            if self.position.y > self.screen.get_height() or self.position.y < 0:
                self.position.y = self.screen.get_height()

            if self.position.y < 0:
                self.position.y = 0
