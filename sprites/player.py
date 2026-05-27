import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()

        # Aparência (placeholder – substituir por sprites)
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)
        self._draw_shape(alive=True)
        self.rect = self.image.get_rect(topleft=(x, y))

        # Física
        self.vel_x: float = 0.0
        self.vel_y: float = 0.0
        self.on_ground: bool = False

        # Stats
        self.alive: bool    = True
        self.score: int     = 0
        self.lives: int     = PLAYER_LIVES
        self.coins: int     = 0

        # Invencibilidade
        self.invincible: bool       = False
        self.invincible_timer: int  = 0

        # Direção
        self.facing_right: bool = True

        # Jump buffer: guarda o input de pulo por N frames
        self._jump_buffer: int  = 0
        # Coyote time: permite pular por N frames após sair de uma borda
        self._coyote_timer: int = 0

    # ── Aparência ─────────────────────────────────────────────────────────────
    def _draw_shape(self, alive: bool = True) -> None:
        self.image.fill((0, 0, 0, 0))
        color = RED if alive else GRAY
        # Chapéu
        pygame.draw.rect(self.image, color, (4, 0, PLAYER_WIDTH - 8, 16))
        # Corpo
        pygame.draw.rect(self.image, BLUE, (0, 16, PLAYER_WIDTH, PLAYER_HEIGHT - 16))
        # Rosto
        pygame.draw.ellipse(self.image, (255, 200, 150), (6, 4, 20, 16))

    # ── Ação de pular ─────────────────────────────────────────────────────────
    def request_jump(self) -> None:
        """Chamado no evento KEYDOWN: armazena intenção de pular por alguns frames."""
        self._jump_buffer = 10

    def _execute_jump(self) -> None:
        self.vel_y          = PLAYER_JUMP_POWER
        self.on_ground      = False
        self._coyote_timer  = 0
        self._jump_buffer   = 0

    # ── Atualização por frame ─────────────────────────────────────────────────
    def update(self, platforms: pygame.sprite.Group) -> None:  # type: ignore[override]
        keys = pygame.key.get_pressed()

        self.vel_x = 0.0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -PLAYER_SPEED
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = PLAYER_SPEED
            self.facing_right = True

        # Coyote time: decrementa quando no ar
        if self.on_ground:
            self._coyote_timer = 6
        elif self._coyote_timer > 0:
            self._coyote_timer -= 1

        # Gravidade
        self.vel_y = min(self.vel_y + PLAYER_GRAVITY, PLAYER_MAX_FALL)

        # Jump buffer: decrementa e executa quando pode pular
        if self._jump_buffer > 0:
            self._jump_buffer -= 1
            if self.on_ground or self._coyote_timer > 0:
                self._execute_jump()

        # Invencibilidade
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

        # Movimento + colisão
        self.rect.x += int(self.vel_x)
        self._collide_horizontal(platforms)
        self.rect.y += int(self.vel_y)
        self.on_ground = False
        self._collide_vertical(platforms)

        # Limite esquerdo do mundo
        if self.rect.left < 0:
            self.rect.left = 0

    def _collide_horizontal(self, platforms: pygame.sprite.Group) -> None:
        for plat in platforms:
            if self.rect.colliderect(plat.rect):
                if self.vel_x > 0:
                    self.rect.right = plat.rect.left
                elif self.vel_x < 0:
                    self.rect.left = plat.rect.right
                self.vel_x = 0.0

    def _collide_vertical(self, platforms: pygame.sprite.Group) -> None:
        for plat in platforms:
            if self.rect.colliderect(plat.rect):
                if self.vel_y > 0:
                    self.rect.bottom = plat.rect.top
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = plat.rect.bottom
                self.vel_y = 0.0

    # ── Dano ──────────────────────────────────────────────────────────────────
    def take_damage(self) -> None:
        if self.invincible:
            return
        self.lives -= 1
        self.invincible = True
        self.invincible_timer = PLAYER_INVINCIBILITY
        if self.lives <= 0:
            self.alive = False

    # ── Coletar moeda ─────────────────────────────────────────────────────────
    def collect_coin(self) -> None:
        self.coins += 1
        self.score += 100
        if self.coins >= 100:
            self.coins -= 100
            self.lives += 1

    # ── Desenho com offset de câmera ──────────────────────────────────────────
    def draw(self, surface: pygame.Surface, camera_offset_x: int = 0) -> None:
        # Piscar durante invencibilidade
        if self.invincible and self.invincible_timer % 10 < 5:
            return
        draw_rect = self.rect.copy()
        draw_rect.x -= camera_offset_x
        surface.blit(self.image, draw_rect)
