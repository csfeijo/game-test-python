from __future__ import annotations
import pygame
from settings import *
from sprites.platform import Platform, MovingPlatform, FlagPole
from sprites.enemy import Enemy
from sprites.coin import Coin, PowerUp
from levels.level_data import LEVEL_1, LEVEL_2, LEVEL_3

LEVELS = [LEVEL_1, LEVEL_2, LEVEL_3]


def load_level(level_index: int):
    """Converte o mapa textual em grupos de sprites e retorna o ponto inicial do jogador."""
    platforms  = pygame.sprite.Group()
    enemies    = pygame.sprite.Group()
    coins      = pygame.sprite.Group()
    powerups   = pygame.sprite.Group()
    flag       = None

    level_map = LEVELS[level_index % len(LEVELS)]
    num_rows  = len(level_map)

    # Empurra o mapa para baixo de forma que o chão fique próximo da base da tela
    v_offset = max(0, SCREEN_HEIGHT - num_rows * TILE_SIZE)

    # Ponto de início: acima do chão (última linha do mapa)
    ground_top   = v_offset + (num_rows - 1) * TILE_SIZE
    player_start = (3 * TILE_SIZE, ground_top - PLAYER_HEIGHT)

    for row_idx, row in enumerate(level_map):
        for col_idx, cell in enumerate(row):
            x = col_idx * TILE_SIZE
            y = v_offset + row_idx * TILE_SIZE

            if cell == "#":
                platforms.add(Platform(x, y))
            elif cell == "P":
                platforms.add(
                    Platform(x, y, TILE_SIZE * 3, TILE_SIZE // 2, (160, 100, 50))
                )
            elif cell == "M":
                platforms.add(
                    MovingPlatform(x, y, vel_x=2.0, vel_y=0.0, distance=128)
                )
            elif cell == "E":
                enemies.add(Enemy(x, y))
            elif cell == "C":
                coins.add(Coin(x, y))
            elif cell == "U":
                powerups.add(PowerUp(x, y, PowerUp.MUSHROOM))
            elif cell == "S":
                powerups.add(PowerUp(x, y, PowerUp.STAR))
            elif cell == "F":
                flag = FlagPole(x, y - 168)

    # Largura total do nível (em pixels)
    level_pixel_width = max(
        (len(row) * TILE_SIZE for row in level_map), default=SCREEN_WIDTH
    )

    return platforms, enemies, coins, powerups, flag, player_start, level_pixel_width
