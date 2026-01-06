from dataclasses import dataclass, field
from arrow import Arrow
import random
import pygame
import math


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

    def update(self, mouse_pos: tuple[int, int]):
        # Update Grouping and distancing of entity
        self.personalSpace()

        for arrow in self.arrows:
            arrow.draw()
            arrow.drawPosition()
            arrow.update(mouse_pos, targetActive=True)

    def applyForceToAll(self, force: pygame.Vector2):
        for arrow in self.arrows:
            arrow.applyForce(force)

    def personalSpace(self):
        for idx, arrow in enumerate(self.arrows):
            # Only enable debug drawing for the first arrow
            debug = idx == 0
            others = self.checkOthersFov(current_arrow=arrow, debug=debug)

            if not others:
                continue
            # Find the closest other arrow within the field of view
            closest_other = None
            min_distance = float("inf")
            for other in others:
                distance_vec = other.position - arrow.position
                distance = distance_vec.length()
                if distance < min_distance:
                    min_distance = distance
                    closest_other = other

            if closest_other:
                # Steer away from the closest other arrow
                steer = arrow.position - closest_other.position
                if steer.length() > 0:
                    steer = steer.normalize()
                arrow.applyForce(steer * 1)

    def checkOthersFov(
        self, current_arrow: Arrow, radius: int = 150, fov: int = 360, debug=False
    ) -> list[Arrow]:
        center = current_arrow.position
        heading = current_arrow.velocity

        others: list[Arrow] = []

        if heading.length() != 0:
            heading = heading.normalize()
        else:
            if debug:
                self.draw_sector_transparent(
                    self.screen, center, heading, radius, fov, detected=False
                )

        for other in self.arrows:
            if other is current_arrow:
                continue
            to_other = other.position - center

            if to_other.length() > radius:
                if debug:
                    self.draw_sector_transparent(
                        self.screen, center, heading, radius, fov, detected=False
                    )
            angle = math.degrees(math.acos(heading.dot(to_other.normalize())))

            if angle < fov / 2:
                if debug:
                    self.draw_sector_transparent(
                        self.screen, center, heading, radius, fov, detected=True
                    )
                others.append(other)
            else:
                if debug:
                    self.draw_sector_transparent(
                        self.screen, center, heading, radius, fov, detected=False
                    )
        return others

    def draw_sector_transparent(
        self, surface, center, heading, radius, fov_deg, detected=False, num_points=30
    ):
        # Set alpha based on detection
        alpha = 50 if not detected else 120
        color = (0, 0, 255, alpha)  # RGBA

        # Create transparent surface
        sector_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)

        angle_start = math.atan2(heading.y, heading.x) - math.radians(fov_deg / 2)
        angle_end = math.atan2(heading.y, heading.x) + math.radians(fov_deg / 2)
        points = [center]
        for i in range(num_points + 1):
            angle = angle_start + (angle_end - angle_start) * i / num_points
            x = center.x + radius * math.cos(angle)
            y = center.y + radius * math.sin(angle)
            points.append((x, y))
        pygame.draw.polygon(sector_surface, color, points, 0)  # 0 for filled
        surface.blit(sector_surface, (0, 0))
