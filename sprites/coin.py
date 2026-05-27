import math
import pygame
from settings import *


class Coin(pygame.sprite.Sprite):
    """Moeda animada coletável (+100 pontos)."""

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self._base_image = self._make_image(1.0)
        self.image = self._base_image
        self.rect  = self.image.get_rect(topleft=(x, y))
        self._tick = 0

    @staticmethod
    def _make_image(scale: float) -> pygame.Surface:
        w = max(4, int(20 * scale))
        surf = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, YELLOW, (10 - w // 2, 0, w, 20))
        pygame.draw.ellipse(surf, ORANGE, (10 - w // 2, 0, w, 20), 2)
        return surf

    def update(self) -> None:  # type: ignore[override]
        self._tick += 1
        scale = abs(math.sin(math.radians(self._tick * 4)))
        self.image = self._make_image(scale)
        self.rect  = self.image.get_rect(center=self.rect.center)


class PowerUp(pygame.sprite.Sprite):
    """Power-up coletável com três variantes."""

    MUSHROOM = "mushroom"
    STAR     = "star"
    FLOWER   = "flower"

    _COLORS = {MUSHROOM: RED, STAR: YELLOW, FLOWER: ORANGE}

    def __init__(self, x: int, y: int, kind: str = MUSHROOM) -> None:
        super().__init__()
        self.kind  = kind
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        self._draw()
        self.rect  = self.image.get_rect(topleft=(x, y))
        self.vel_x: float = 1.0
        self.vel_y: float = 0.0

    def _draw(self) -> None:
        color = self._COLORS.get(self.kind, RED)
        pygame.draw.circle(self.image, color, (TILE_SIZE // 2, TILE_SIZE // 2), TILE_SIZE // 2)
        pygame.draw.circle(self.image, WHITE, (TILE_SIZE // 2, TILE_SIZE // 2), TILE_SIZE // 2, 2)
        # letra identificadora
        font = pygame.font.SysFont("Arial", 16, bold=True)
        label = font.render(self.kind[0].upper(), True, WHITE)
        self.image.blit(label, label.get_rect(center=(TILE_SIZE // 2, TILE_SIZE // 2)))

    def apply(self, player) -> None:  # type: ignore[no-untyped-def]
        if self.kind == self.MUSHROOM:
            player.lives += 1
        elif self.kind == self.STAR:
            player.invincible       = True
            player.invincible_timer = 600
        elif self.kind == self.FLOWER:
            player.score += 1000

    def update(self, platforms: pygame.sprite.Group) -> None:  # type: ignore[override]
        self.vel_y = min(self.vel_y + PLAYER_GRAVITY, PLAYER_MAX_FALL)
        self.rect.x += int(self.vel_x)
        self.rect.y += int(self.vel_y)

        for plat in platforms:
            if self.rect.colliderect(plat.rect):
                if self.vel_y > 0:
                    self.rect.bottom = plat.rect.top
                    self.vel_y = 0.0
                self.vel_x = -self.vel_x
