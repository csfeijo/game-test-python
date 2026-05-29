from __future__ import annotations
import sys
import pygame
from settings import *
from sprites.player import Player
from sprites.coin import Coin
from ui.hud import HUD
from levels.level_manager import load_level

LEVEL_TIME = 300   # segundos por fase


class Camera:
    def __init__(self, level_width: int) -> None:
        self.offset_x    = 0
        self.level_width = level_width

    def update(self, player: Player) -> None:
        target        = player.rect.centerx - SCREEN_WIDTH // 2
        self.offset_x = max(0, min(target, self.level_width - SCREEN_WIDTH))


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock   = pygame.time.Clock()
        self.hud     = HUD()
        self.state   = STATE_MENU
        self.level_index = 0

        self._font_title = pygame.font.SysFont("Arial", 52, bold=True)
        self._font_sub   = pygame.font.SysFont("Arial", 26)

        # Atributos declarados (instanciados em _load_level)
        self.player:         Player
        self.camera:         Camera
        self.platforms:      pygame.sprite.Group
        self.enemies:        pygame.sprite.Group
        self.coins:          pygame.sprite.Group
        self.powerups:       pygame.sprite.Group
        self.question_tiles: pygame.sprite.Group
        self.flag:           object | None
        self.time_left:      float
        self._time_acc:      float

    # ── Gestão de nível ───────────────────────────────────────────────────────
    def _new_game(self) -> None:
        self.level_index = 0
        self._load_level()

    def _load_level(self) -> None:
        (
            self.platforms,
            self.enemies,
            self.coins,
            self.powerups,
            self.question_tiles,
            self.flag,
            player_start,
            level_width,
        ) = load_level(self.level_index)

        self._player_start = player_start
        self.player        = Player(*player_start)
        self.camera        = Camera(level_width)
        self.time_left     = float(LEVEL_TIME)
        self._time_acc     = 0.0
        self.state         = STATE_PLAYING

    # ── Eventos ───────────────────────────────────────────────────────────────
    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if self.state == STATE_MENU:
                    if event.key == pygame.K_RETURN:
                        self._new_game()

                elif self.state == STATE_PLAYING:
                    if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                        self.player.request_jump()
                    if event.key == pygame.K_ESCAPE:
                        self.state = STATE_PAUSED

                elif self.state == STATE_PAUSED:
                    if event.key == pygame.K_ESCAPE:
                        self.state = STATE_PLAYING

                elif self.state in (STATE_GAME_OVER, STATE_LEVEL_COMPLETE):
                    if event.key == pygame.K_RETURN:
                        self.state = STATE_MENU

            if event.type == pygame.KEYUP:
                if self.state == STATE_PLAYING:
                    if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                        self.player.cut_jump()

    # ── Update ────────────────────────────────────────────────────────────────
    def _update(self) -> None:
        if self.state != STATE_PLAYING:
            return

        dt             = self.clock.get_time() / 1000.0
        self.time_left = max(0.0, self.time_left - dt)

        if self.time_left <= 0:
            self.player.take_damage()
            if not self.player.alive:
                self.state = STATE_GAME_OVER
            else:
                self._load_level()
            return

        # Player
        self.player.update(self.platforms)

        # Plataformas móveis
        from sprites.platform import MovingPlatform
        for plat in self.platforms:
            if isinstance(plat, MovingPlatform):
                plat.update()

        # Entidades
        self.enemies.update(self.platforms)
        self.coins.update()
        self.powerups.update(self.platforms)

        # Question tiles — animação + spawn de moeda
        for qt in self.question_tiles:
            qt.update()
            if qt.pop_coin():
                new_coin = Coin(qt.rect.x, qt.rect.y - TILE_SIZE)
                self.coins.add(new_coin)
                self.player.score += SCORE_COIN

        self.camera.update(self.player)

        # Colisões
        self._check_enemy_collisions()
        self._check_coin_collisions()
        self._check_powerup_collisions()
        self._check_flag_collision()
        self._check_fall_off()

    # ── Colisões de gameplay ──────────────────────────────────────────────────
    def _check_enemy_collisions(self) -> None:
        for enemy in list(self.enemies):
            if not enemy.stomped and self.player.rect.colliderect(enemy.rect):
                if (self.player.vel_y > 0
                        and self.player.rect.bottom < enemy.rect.centery + 8):
                    enemy.get_stomped()
                    self.player.vel_y  = PLAYER_JUMP_POWER * 0.55
                    self.player.score += SCORE_ENEMY
                else:
                    self.player.take_damage()
                    if not self.player.alive:
                        self.state = STATE_GAME_OVER

    def _check_coin_collisions(self) -> None:
        for _ in pygame.sprite.spritecollide(self.player, self.coins, True):
            self.player.collect_coin()

    def _check_powerup_collisions(self) -> None:
        for pu in pygame.sprite.spritecollide(self.player, self.powerups, True):
            pu.apply(self.player)
            self.player.score += SCORE_POWERUP

    def _check_flag_collision(self) -> None:
        if self.flag and self.player.rect.colliderect(self.flag.rect):
            self.player.score += int(self.time_left) * SCORE_TIME_FACTOR
            self.level_index  += 1
            self.state = STATE_LEVEL_COMPLETE

    def _check_fall_off(self) -> None:
        if self.player.rect.top > SCREEN_HEIGHT + 32:
            self.player.take_damage()
            if not self.player.alive:
                self.state = STATE_GAME_OVER
            else:
                self.player.rect.topleft = self._player_start
                self.player.vel_x        = 0.0
                self.player.vel_y        = 0.0

    # ── Render ────────────────────────────────────────────────────────────────
    def _draw(self) -> None:
        self.screen.fill(SKY_BLUE)
        if self.state in (STATE_PLAYING, STATE_PAUSED):
            self._draw_world(self.camera.offset_x)
            self.hud.draw(self.screen, self.player, self.level_index, self.time_left)
            if self.state == STATE_PAUSED:
                self._draw_overlay("PAUSADO", "ESC para continuar")
        elif self.state == STATE_MENU:
            self._draw_menu()
        elif self.state == STATE_GAME_OVER:
            self._draw_overlay("GAME OVER", "ENTER para voltar ao menu")
        elif self.state == STATE_LEVEL_COMPLETE:
            self._draw_overlay(
                f"FASE {self.level_index} COMPLETA!", "ENTER para continuar"
            )
        pygame.display.flip()

    def _draw_world(self, ox: int) -> None:
        def blit(sprite):
            r   = sprite.rect.copy()
            r.x -= ox
            self.screen.blit(sprite.image, r)

        for plat in self.platforms:
            blit(plat)
        if self.flag:
            blit(self.flag)
        for coin in self.coins:
            blit(coin)
        for pu in self.powerups:
            blit(pu)
        for enemy in self.enemies:
            blit(enemy)
        self.player.draw(self.screen, ox)

    def _draw_menu(self) -> None:
        cx       = SCREEN_WIDTH // 2
        title    = self._font_title.render("SUPER THÉO", True, YELLOW)
        subtitle = self._font_sub.render("Pressione ENTER para jogar", True, WHITE)
        controls = self._font_sub.render(
            "A/D  ← →  mover   |   ESPAÇO / ↑  pular   |   ESC  pausar",
            True, WHITE,
        )
        self.screen.blit(title,    title.get_rect(center=(cx, SCREEN_HEIGHT // 2 - 80)))
        self.screen.blit(subtitle, subtitle.get_rect(center=(cx, SCREEN_HEIGHT // 2)))
        self.screen.blit(controls, controls.get_rect(center=(cx, SCREEN_HEIGHT // 2 + 60)))

    def _draw_overlay(self, title: str, subtitle: str) -> None:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))
        cx     = SCREEN_WIDTH // 2
        t_surf = self._font_title.render(title,    True, YELLOW)
        s_surf = self._font_sub.render(subtitle,   True, WHITE)
        self.screen.blit(t_surf, t_surf.get_rect(center=(cx, SCREEN_HEIGHT // 2 - 40)))
        self.screen.blit(s_surf, s_surf.get_rect(center=(cx, SCREEN_HEIGHT // 2 + 30)))

    # ── Loop principal ────────────────────────────────────────────────────────
    def run(self) -> None:
        while True:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)
