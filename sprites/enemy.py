import pygame
from settings import *


class Enemy(pygame.sprite.Sprite):
    """Inimigo básico estilo Goomba: anda horizontalmente e reverte ao colidir."""

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.image = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT), pygame.SRCALPHA)
        self._draw_normal()
        self.rect = self.image.get_rect(topleft=(x, y))

        self.vel_x: float = -ENEMY_SPEED
        self.vel_y: float = 0.0
        self.stomped: bool  = False
        self.stomp_timer: int = 0

    # ── Aparência ─────────────────────────────────────────────────────────────
    def _draw_normal(self) -> None:
        self.image.fill((0, 0, 0, 0))
        pygame.draw.ellipse(self.image, BROWN, (2, 8, ENEMY_WIDTH - 4, ENEMY_HEIGHT - 8))
        # olhos
        pygame.draw.circle(self.image, WHITE, (9, 14), 5)
        pygame.draw.circle(self.image, WHITE, (ENEMY_WIDTH - 9, 14), 5)
        pygame.draw.circle(self.image, BLACK, (9, 14), 2)
        pygame.draw.circle(self.image, BLACK, (ENEMY_WIDTH - 9, 14), 2)
        # pés
        pygame.draw.ellipse(self.image, BROWN, (0, ENEMY_HEIGHT - 12, 16, 12))
        pygame.draw.ellipse(self.image, BROWN, (ENEMY_WIDTH - 16, ENEMY_HEIGHT - 12, 16, 12))

    def _draw_stomped(self) -> None:
        self.image.fill((0, 0, 0, 0))
        pygame.draw.ellipse(self.image, BROWN, (2, ENEMY_HEIGHT // 2, ENEMY_WIDTH - 4, ENEMY_HEIGHT // 2))

    # ── Atualização ───────────────────────────────────────────────────────────
    def update(self, platforms: pygame.sprite.Group) -> None:  # type: ignore[override]
        if self.stomped:
            self.stomp_timer -= 1
            if self.stomp_timer <= 0:
                self.kill()
            return

        self.vel_y = min(self.vel_y + PLAYER_GRAVITY, PLAYER_MAX_FALL)

        self.rect.x += int(self.vel_x)
        self._collide_horizontal(platforms)

        self.rect.y += int(self.vel_y)
        self._collide_vertical(platforms)

    def _collide_horizontal(self, platforms: pygame.sprite.Group) -> None:
        for plat in platforms:
            if self.rect.colliderect(plat.rect):
                self.vel_x = -self.vel_x
                if self.vel_x > 0:
                    self.rect.left = plat.rect.right
                else:
                    self.rect.right = plat.rect.left

    def _collide_vertical(self, platforms: pygame.sprite.Group) -> None:
        for plat in platforms:
            if self.rect.colliderect(plat.rect):
                if self.vel_y > 0:
                    self.rect.bottom = plat.rect.top
                elif self.vel_y < 0:
                    self.rect.top = plat.rect.bottom
                self.vel_y = 0.0

    # ── Pisar no inimigo ──────────────────────────────────────────────────────
    def get_stomped(self) -> None:
        self.stomped = True
        self.stomp_timer = 30
        self._draw_stomped()
        self.rect.height = ENEMY_HEIGHT // 2
        self.rect.y += ENEMY_HEIGHT // 2
