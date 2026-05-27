import pygame
from settings import *


class HUD:
    """Exibe pontuação, moedas, vidas, fase e tempo na tela."""

    def __init__(self) -> None:
        pygame.font.init()
        self._font_lg = pygame.font.SysFont("Arial", 26, bold=True)
        self._font_sm = pygame.font.SysFont("Arial", 20)

    def draw(
        self,
        surface: pygame.Surface,
        player,
        level_index: int,
        time_left: float,
    ) -> None:
        # Fundo semi-transparente
        bar = pygame.Surface((SCREEN_WIDTH, 44), pygame.SRCALPHA)
        bar.fill((0, 0, 0, 140))
        surface.blit(bar, (0, 0))

        items = [
            (self._font_lg, f"SCORE  {player.score:06d}", WHITE,  20),
            (self._font_sm, f"x{player.coins:02d}",       YELLOW, 260),
            (self._font_sm, f"VIDAS {player.lives}",      WHITE,  340),
            (self._font_sm, f"MUNDO {level_index + 1}-1", WHITE,  500),
            (self._font_sm, f"TEMPO {int(time_left):03d}", WHITE,  660),
        ]

        # Ícone de moeda
        pygame.draw.circle(surface, YELLOW, (248, 22), 9)

        for font, text, color, x in items:
            surf = font.render(text, True, color)
            surface.blit(surf, (x, 12))
