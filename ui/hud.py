import pygame
from settings import *

_HEART       = "\u2665"
_WARN_TIME   = 60      # segundos em que o tempo começa a piscar vermelho
_BLINK_RATE  = 30      # frames entre piscadas


class HUD:
    """Exibe pontuação, moedas, vidas, fase e tempo na tela."""

    def __init__(self) -> None:
        pygame.font.init()
        self._font_lg   = pygame.font.SysFont("Arial", 26, bold=True)
        self._font_sm   = pygame.font.SysFont("Arial", 20)
        self._font_icon = pygame.font.SysFont("Arial", 18)
        self._frame     = 0

    def draw(
        self,
        surface: pygame.Surface,
        player,
        level_index: int,
        time_left: float,
    ) -> None:
        self._frame += 1

        # Fundo semi-transparente
        bar = pygame.Surface((SCREEN_WIDTH, 44), pygame.SRCALPHA)
        bar.fill((0, 0, 0, 150))
        surface.blit(bar, (0, 0))

        # ── Pontuação ──────────────────────────────────────────────────────
        score_surf = self._font_lg.render(f"{player.score:06d}", True, WHITE)
        surface.blit(score_surf, (20, 10))

        # ── Moedas ─────────────────────────────────────────────────────────
        pygame.draw.circle(surface, YELLOW, (210, 22), 9)
        coin_surf = self._font_sm.render(f"x{player.coins:02d}", True, YELLOW)
        surface.blit(coin_surf, (224, 12))

        # ── Vidas (corações) ───────────────────────────────────────────────
        lives_label = self._font_sm.render("VIDAS", True, WHITE)
        surface.blit(lives_label, (340, 12))
        for i in range(player.lives):
            h = self._font_icon.render(_HEART, True, RED)
            surface.blit(h, (405 + i * 22, 13))

        # ── Fase ───────────────────────────────────────────────────────────
        world_surf = self._font_sm.render(f"MUNDO {level_index + 1}-1", True, WHITE)
        surface.blit(world_surf, (540, 12))

        # ── Tempo (pisca vermelho quando crítico) ──────────────────────────
        urgent      = time_left <= _WARN_TIME
        blink_off   = urgent and (self._frame % _BLINK_RATE < _BLINK_RATE // 2)
        time_color  = RED if urgent else WHITE
        if not blink_off:
            time_surf = self._font_sm.render(f"TEMPO {int(time_left):03d}", True, time_color)
            surface.blit(time_surf, (670, 12))
