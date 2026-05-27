import pygame
from settings import *


class Platform(pygame.sprite.Sprite):
    """Bloco/plataforma estático."""

    def __init__(
        self,
        x: int,
        y: int,
        width: int  = TILE_SIZE,
        height: int = TILE_SIZE,
        color: tuple = GREEN,
    ) -> None:
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        # Borda escura
        pygame.draw.rect(self.image, BLACK, self.image.get_rect(), 2)
        # Brilho superior
        pygame.draw.line(self.image, WHITE, (1, 1), (width - 2, 1), 2)
        self.rect = self.image.get_rect(topleft=(x, y))


class MovingPlatform(Platform):
    """Plataforma que se move em linha reta e reverte ao atingir a distância máxima."""

    def __init__(
        self,
        x: int,
        y: int,
        width: int  = TILE_SIZE * 3,
        height: int = TILE_SIZE // 2,
        vel_x: float = 2.0,
        vel_y: float = 0.0,
        distance: int = 120,
    ) -> None:
        super().__init__(x, y, width, height, (100, 180, 100))
        self.vel_x    = vel_x
        self.vel_y    = vel_y
        self.distance = distance
        self.traveled = 0.0

    def update(self) -> None:  # type: ignore[override]
        self.rect.x += int(self.vel_x)
        self.rect.y += int(self.vel_y)
        self.traveled += abs(self.vel_x) + abs(self.vel_y)
        if self.traveled >= self.distance:
            self.vel_x = -self.vel_x
            self.vel_y = -self.vel_y
            self.traveled = 0.0


class FlagPole(pygame.sprite.Sprite):
    """Bandeira no final da fase."""

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.image = pygame.Surface((12, 200), pygame.SRCALPHA)
        pygame.draw.rect(self.image, GRAY, (4, 0, 4, 200))   # mastro
        pygame.draw.polygon(                                   # bandeira
            self.image, GREEN,
            [(8, 0), (8, 28), (30, 14)],
        )
        self.rect = self.image.get_rect(topleft=(x, y))
