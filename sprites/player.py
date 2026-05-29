import pygame
from settings import *

# ── Estados do jogador ────────────────────────────────────────────────────────
PSTATE_IDLE    = "idle"
PSTATE_WALKING = "walking"
PSTATE_JUMPING = "jumping"
PSTATE_FALLING = "falling"
PSTATE_DEAD    = "dead"


class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()

        # alive precisa ser definido antes de _draw_shape()
        self.alive: bool = True

        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)
        self._draw_shape()
        self.rect = self.image.get_rect(topleft=(x, y))

        # Física
        self.vel_x: float = 0.0
        self.vel_y: float = 0.0
        self.on_ground: bool = False

        # Estado
        self._state: str = PSTATE_IDLE

        # Stats
        self.score: int = 0
        self.lives: int = PLAYER_LIVES
        self.coins: int = 0

        # Invencibilidade
        self.invincible: bool      = False
        self.invincible_timer: int = 0

        # Direção
        self.facing_right: bool = True

        # Jump mechanics
        self._jump_buffer: int  = 0
        self._coyote_timer: int = 0

    # ── Estado ────────────────────────────────────────────────────────────────
    @property
    def state(self) -> str:
        return self._state

    def _update_state(self) -> None:
        if not self.alive:
            self._state = PSTATE_DEAD
        elif not self.on_ground:
            self._state = PSTATE_JUMPING if self.vel_y < 0 else PSTATE_FALLING
        elif abs(self.vel_x) > 0.2:
            self._state = PSTATE_WALKING
        else:
            self._state = PSTATE_IDLE

    # ── Aparência ─────────────────────────────────────────────────────────────
    def _draw_shape(self) -> None:
        self.image.fill((0, 0, 0, 0))
        color = RED if self.alive else GRAY
        # Chapéu
        pygame.draw.rect(self.image, color, (4, 0, PLAYER_WIDTH - 8, 16))
        # Corpo
        pygame.draw.rect(self.image, BLUE, (0, 16, PLAYER_WIDTH, PLAYER_HEIGHT - 16))
        # Rosto
        pygame.draw.ellipse(self.image, (255, 200, 150), (6, 4, 20, 16))

    # ── Pulo ──────────────────────────────────────────────────────────────────
    def request_jump(self) -> None:
        """Chamado no KEYDOWN: armazena intenção de pular por alguns frames."""
        self._jump_buffer = 10

    def cut_jump(self) -> None:
        """Chamado no KEYUP: pulo variável — soltar cedo = pulo menor."""
        if self.vel_y < 0:
            self.vel_y *= PLAYER_JUMP_CUT

    def _execute_jump(self) -> None:
        self.vel_y         = PLAYER_JUMP_POWER
        self.on_ground     = False
        self._coyote_timer = 0
        self._jump_buffer  = 0

    # ── Atualização por frame ─────────────────────────────────────────────────
    def update(self, platforms: pygame.sprite.Group) -> None:  # type: ignore[override]
        if not self.alive:
            return

        keys = pygame.key.get_pressed()

        # Coyote time
        if self.on_ground:
            self._coyote_timer = 6
        elif self._coyote_timer > 0:
            self._coyote_timer -= 1

        # Movimento horizontal com aceleração
        accel    = PLAYER_ACCEL if self.on_ground else PLAYER_ACCEL * PLAYER_AIR_CONTROL
        pressing = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x        = max(-PLAYER_MAX_SPEED, self.vel_x - accel)
            self.facing_right = False
            pressing          = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x        = min(PLAYER_MAX_SPEED, self.vel_x + accel)
            self.facing_right = True
            pressing          = True

        if not pressing:
            if self.on_ground:
                self.vel_x *= PLAYER_FRICTION
                if abs(self.vel_x) < 0.15:
                    self.vel_x = 0.0
            else:
                self.vel_x *= 0.99  # resistência mínima no ar

        # Gravidade assimétrica (sobe suave, cai rápido — arco Mario)
        if self.vel_y < 0:
            self.vel_y = min(self.vel_y + PLAYER_GRAVITY, PLAYER_MAX_FALL)
        else:
            self.vel_y = min(self.vel_y + PLAYER_FALL_GRAVITY, PLAYER_MAX_FALL)

        # Jump buffer
        if self._jump_buffer > 0:
            self._jump_buffer -= 1
            if self.on_ground or self._coyote_timer > 0:
                self._execute_jump()

        # Invencibilidade
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

        # Colisão
        self.rect.x += int(self.vel_x)
        self._collide_horizontal(platforms)
        self.rect.y += int(self.vel_y)
        self.on_ground = False
        self._collide_vertical(platforms)

        # Limite esquerdo do mundo
        if self.rect.left < 0:
            self.rect.left = 0
            self.vel_x     = 0.0

        self._update_state()

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
                    self.on_ground   = True
                elif self.vel_y < 0:
                    self.rect.top = plat.rect.bottom
                    # Notifica bloco surpresa (QuestionTile)
                    if hasattr(plat, 'bump'):
                        plat.bump()
                self.vel_y = 0.0

    # ── Dano ──────────────────────────────────────────────────────────────────
    def take_damage(self) -> None:
        if self.invincible:
            return
        self.lives -= 1
        self.invincible       = True
        self.invincible_timer = PLAYER_INVINCIBILITY
        if self.lives <= 0:
            self.alive = False

    # ── Coletar moeda ─────────────────────────────────────────────────────────
    def collect_coin(self) -> None:
        self.coins  += 1
        self.score  += SCORE_COIN
        if self.coins >= 100:
            self.coins -= 100
            self.lives += 1

    # ── Desenho com offset de câmera ──────────────────────────────────────────
    def draw(self, surface: pygame.Surface, camera_offset_x: int = 0) -> None:
        if self.invincible and self.invincible_timer % 10 < 5:
            return
        draw_rect   = self.rect.copy()
        draw_rect.x -= camera_offset_x
        surface.blit(self.image, draw_rect)
