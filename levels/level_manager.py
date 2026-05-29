from __future__ import annotations
import pygame
from settings import *
from sprites.platform import Platform, MovingPlatform, FlagPole
from sprites.tiles import SolidTile, BrickTile, QuestionTile, PipeTile
from sprites.enemy import Enemy
from sprites.coin import Coin, PowerUp
from levels.level_data import LEVEL_1, LEVEL_2, LEVEL_3

LEVELS = [LEVEL_1, LEVEL_2, LEVEL_3]


def load_level(level_index: int):
    """
    Retorna 8 valores:
      platforms, enemies, coins, powerups,
      question_tiles, flag, player_start, level_pixel_width

    Mapa de caracteres
    ------------------
    # / G  → SolidTile (chão / blocos genéricos)
    B      → BrickTile
    Q      → QuestionTile
    P      → PipeTile  (2×2, usa posição top-left do cano)
    E      → Enemy
    C      → Coin
    U      → PowerUp (cogumelo)
    S      → PowerUp (estrela)
    F      → FlagPole
    """
    platforms      = pygame.sprite.Group()
    enemies        = pygame.sprite.Group()
    coins          = pygame.sprite.Group()
    powerups       = pygame.sprite.Group()
    question_tiles = pygame.sprite.Group()
    flag           = None

    level_map  = LEVELS[level_index % len(LEVELS)]
    num_rows   = len(level_map)
    v_offset   = max(0, SCREEN_HEIGHT - num_rows * TILE_SIZE)
    ground_top = v_offset + (num_rows - 1) * TILE_SIZE

    player_start: tuple[int, int] = (3 * TILE_SIZE, ground_top - PLAYER_HEIGHT)

    # evita duplicar tiles de cano que ocupam 2×2
    pipe_positions: set[tuple[int, int]] = set()

    for row_idx, row in enumerate(level_map):
        for col_idx, cell in enumerate(row):
            x = col_idx * TILE_SIZE
            y = v_offset + row_idx * TILE_SIZE

            if cell in ('#', 'G'):
                platforms.add(SolidTile(x, y))

            elif cell == 'B':
                platforms.add(BrickTile(x, y))

            elif cell == 'Q':
                qt = QuestionTile(x, y)
                platforms.add(qt)
                question_tiles.add(qt)

            elif cell == 'P':
                pos = (col_idx, row_idx)
                if pos not in pipe_positions:
                    pipe_positions.add(pos)
                    platforms.add(PipeTile(x, y))

            elif cell == 'E':
                enemies.add(Enemy(x, y))

            elif cell == 'C':
                coins.add(Coin(x, y))

            elif cell == 'U':
                powerups.add(PowerUp(x, y, PowerUp.MUSHROOM))

            elif cell == 'S':
                powerups.add(PowerUp(x, y, PowerUp.STAR))

            elif cell == 'F':
                flag = FlagPole(x, y - 168)

    level_pixel_width = max(
        (len(row) * TILE_SIZE for row in level_map),
        default=SCREEN_WIDTH,
    )
    return (
        platforms,
        enemies,
        coins,
        powerups,
        question_tiles,
        flag,
        player_start,
        level_pixel_width,
    )
