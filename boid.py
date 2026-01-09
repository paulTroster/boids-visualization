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

            # Give random initial velocity
            import math

            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(5, 10)
            initial_velocity = pygame.Vector2(
                math.cos(angle) * speed, math.sin(angle) * speed
            )

            arrow = Arrow(self.screen, position, scale=0.2, velocity=initial_velocity)
            self.arrows.append(arrow)

    def update(self, mouse_pos: tuple[int, int]):
        # Update Grouping and distancing of entity
        self.personalSpace()
        self.applyGroupCenter()

        for arrow in self.arrows:
            arrow.draw()
            arrow.drawPosition()
            arrow.update(mouse_pos, targetActive=False)

    def applyForceToAll(self, force: pygame.Vector2):
        for arrow in self.arrows:
            arrow.applyForce(force)

    def personalSpace(self):
        for idx, arrow in enumerate(self.arrows):
            # Only enable debug drawing for the first arrow
            debug = idx == 0
            closest_other, detected = self.findClosestInFov(
                current_arrow=arrow, debug=debug
            )

            if closest_other:
                # Steer away from the closest other arrow
                steer = arrow.position - closest_other.position
                distance = steer.length()
                if distance > 0:
                    steer.normalize_ip()  # In-place normalization
                    # Scale force by inverse distance (stronger when closer)
                    force_magnitude = min(1.0 / (distance / 50), 0.5)
                    arrow.applyForce(steer * force_magnitude)

    def applyGroupCenter(self, radius: int = 150, fov: int = 100) -> None:
        for idx, arrow in enumerate(self.arrows):
            # Get all arrows in pov
            others = self.findArrowsInFov(arrow, radius, fov)

            if len(others) == 0:
                continue

            # calculate midpoint of all vectors
            midpoint = sum(
                [arrow.position for arrow in others], pygame.Vector2(0, 0)
            ) / len(others)

            if debug and idx == 0:
                pygame.draw.circle(self.screen, "green", midpoint, 10)

            direction = midpoint - arrow.position
            distance = direction.length()
            
            if distance > 0:
                direction.normalize_ip()
                # Scale force - stronger when further, but capped
                force_magnitude = min(distance / 200, 0.3)
                arrow.applyForce(direction * force_magnitude)
            
            # Apply force towards this direction
            arrow.applyForce(direction)

    def findClosestInFov(
        self, current_arrow: Arrow, radius: int = 150, fov: int = 100, debug=False
    ) -> tuple[Arrow | None, bool]:
        center = current_arrow.position
        heading = current_arrow.velocity
        heading_length_sq = heading.length_squared()

        if heading_length_sq == 0:
            if debug:
                self.draw_sector_transparent(
                    self.screen,
                    center,
                    pygame.Vector2(1, 0),
                    radius,
                    fov,
                    detected=False,
                )
            return None, False

        heading = heading / math.sqrt(
            heading_length_sq
        )  # Normalize using cached length_squared

        closest_other = None
        min_distance_sq = float("inf")
        detected = False

        for other in self.findArrowsInFov(current_arrow, radius, fov):

            to_other = other.position - center
            distance_sq = to_other.length_squared()

            detected = True
            if distance_sq < min_distance_sq:
                min_distance_sq = distance_sq
                closest_other = other

        if debug:
            self.draw_sector_transparent(
                self.screen, center, heading, radius, fov, detected=detected
            )

        return closest_other, detected

    def findArrowsInFov(
        self, current_arrow: Arrow, radius: int, fov: int
    ) -> list[Arrow]:

        center = current_arrow.position
        heading = current_arrow.velocity
        heading_length_sq = heading.length_squared()
        radius_sq = radius * radius

        heading = heading / math.sqrt(
            heading_length_sq
        )  # Normalize using cached length_squared

        fov_half = fov / 2

        in_fov = []

        for other in self.arrows:
            if other is current_arrow:
                continue

            to_other = other.position - center
            distance_sq = to_other.length_squared()

            # Early exit if outside radius
            if distance_sq > radius_sq:
                continue

            # Check FOV
            distance = math.sqrt(distance_sq)
            to_other_norm = to_other / distance
            angle = math.degrees(math.acos(max(-1, min(1, heading.dot(to_other_norm)))))

            if angle < fov_half:
                in_fov.append(other)

        return in_fov

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
