import pygame
from settings import *

# ── Paleta dos tiles ──────────────────────────────────────────────────────────
COLOR_GROUND = (80,  120,  50)
COLOR_BRICK  = (165,  82,  40)
COLOR_QBLOCK = (230, 180,  10)
COLOR_USED   = (100, 100, 100)
COLOR_PIPE   = ( 20, 140,  20)


class SolidTile(pygame.sprite.Sprite):
    """Tile sólido base — colisão em todos os lados."""

    solid = True

    def __init__(self, x, y, color=COLOR_GROUND, width=TILE_SIZE, height=TILE_SIZE):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        pygame.draw.rect(self.image, BLACK, self.image.get_rect(), 2)
        pygame.draw.line(self.image, WHITE, (1, 1), (width - 2, 1), 1)
        self.rect    = self.image.get_rect(topleft=(x, y))
        self._base_x = x
        self._base_y = y


class BrickTile(SolidTile):
    """Bloco de tijolo com padrão desenhado."""

    def __init__(self, x, y):
        super().__init__(x, y, COLOR_BRICK)
        for ly in (10, 21):
            pygame.draw.line(self.image, BLACK, (0, ly), (TILE_SIZE, ly), 1)
        for lx, y0, y1 in ((16, 0, 10), (8, 10, 21), (16, 21, TILE_SIZE)):
            pygame.draw.line(self.image, BLACK, (lx, y0), (lx, y1), 1)


class QuestionTile(SolidTile):
    """Bloco surpresa: anima ao ser batido por baixo, libera moeda e vira usado."""

    _RISE_FRAMES = 10
    _FALL_FRAMES = 10
    _BUMP_PIXELS = 6

    def __init__(self, x, y):
        super().__init__(x, y, COLOR_QBLOCK)
        self._draw_question_mark()
        self.activated    = False
        self._phase       = 0     # 0=idle  1=subindo  2=voltando
        self._timer       = 0
        self._coin_ready  = False

    def _draw_question_mark(self):
        pygame.font.init()
        font  = pygame.font.SysFont("Arial", 20, bold=True)
        label = font.render("?", True, WHITE)
        self.image.blit(label, label.get_rect(center=(TILE_SIZE // 2, TILE_SIZE // 2)))

    def bump(self):
        """Chamado pelo jogador ao bater por baixo."""
        if self.activated or self._phase != 0:
            return
        self._phase      = 1
        self._timer      = self._RISE_FRAMES
        self._coin_ready = True

    def pop_coin(self):
        """Retorna True uma única vez para spawnar uma moeda."""
        if self._coin_ready:
            self._coin_ready = False
            return True
        return False

    def update(self):
        if self._phase == 0:
            return
        if self._phase == 1:   # subindo
            self._timer -= 1
            progress    = 1.0 - self._timer / self._RISE_FRAMES
            self.rect.y = self._base_y - int(self._BUMP_PIXELS * progress)
            if self._timer <= 0:
                self.rect.y = self._base_y - self._BUMP_PIXELS
                self._phase = 2
                self._timer = self._FALL_FRAMES
        elif self._phase == 2:  # voltando
            self._timer -= 1
            progress    = self._timer / self._FALL_FRAMES
            self.rect.y = self._base_y - int(self._BUMP_PIXELS * progress)
            if self._timer <= 0:
                self.rect.y = self._base_y
                self._phase = 0
                if not self.activated:
                    self.activated = True
                    self._become_used()

    def _become_used(self):
        self.image.fill(COLOR_USED)
        pygame.draw.rect(self.image, BLACK, self.image.get_rect(), 2)


class UsedTile(SolidTile):
    """Bloco já ativado — sem interação."""

    def __init__(self, x, y):
        super().__init__(x, y, COLOR_USED)


class PipeTile(SolidTile):
    """Cano verde sólido (2×2 tiles)."""

    def __init__(self, x, y):
        w, h = TILE_SIZE * 2, TILE_SIZE * 2
        super().__init__(x, y, COLOR_PIPE, width=w, height=h)
        dark = (10, 100, 10)
        pygame.draw.rect(self.image, dark,       self.image.get_rect(), 3)
        pygame.draw.rect(self.image, dark,       (0, 0, w, 14))
        pygame.draw.rect(self.image, COLOR_PIPE, (4, 2, w - 8, 10))
