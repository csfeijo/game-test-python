# ──────────────────────────────────────────────────────────────────────────────
# Mapa de nível — 18 linhas × N colunas (cada char = 1 tile de 32×32 px)
# v_offset = max(0, 600 - 18*32) = 24 px   →   chão no row 17 (y = 568)
#
# Caracteres
# ──────────────────────────────────────────────────────────────────────────────
#   #  SolidTile (chão)         B  BrickTile (plataforma)
#   Q  QuestionTile (bloco ?)   P  PipeTile 2×2 (top-esq, row 15 = flush no chão)
#   E  Enemy (Goomba)           C  Coin
#   U  Power-up (cogumelo)      S  Power-up (estrela)
#   F  FlagPole (fim de fase)   (espaço) = vazio
# ──────────────────────────────────────────────────────────────────────────────
# Acessibilidade (pulo de 195 px a partir do chão):
#   Plataformas saltáveis do chão:  rows 11–16
#   Blocos-Q bativeis do chão:       rows  9–16
#   Row 15 = cano P flush com chão  (y 504-568)
#   Row 16 = inimigos no nível do chão
# ──────────────────────────────────────────────────────────────────────────────

# ── Fase 1 — Verde Hills (fácil, 120 colunas) ────────────────────────────────
# Layout em 3 zonas:
#   Cols  0-40 : zona inicial — chão plano, primeiros inimigos
#   Cols 40-80 : zona de plataformas — bricks + blocos-Q acessíveis do chão
#   Cols 80-120: zona final — cano, inimigos e bandeira
# Plataformas:
#   Row 12: BBBBBBB em cols 42-48 e 78-84  (tier 1, direto do chão)
#   Row  8: BBBBBBB em cols 16-22           (tier 2, do tier 1)
# Blocos-Q:
#   Row 10: Q  Q  Q em cols 32,35,38 (bativeis do chão)
#   Row  7: Q  Q  Q em cols 22,25,28 (bativeis do tier 2) + cogumelo
# Canos: cols 20, 56, 90   Bandeira: col 116
LEVEL_1 = [
    "                                                                                                                        ",  # 0  céu
    "                                                                                                                        ",  # 1  céu
    "                                                                                                                        ",  # 2  céu
    "                                                                                                                        ",  # 3  céu
    "                                                                                                                        ",  # 4  céu
    "                                                                                                                        ",  # 5  céu
    "                      C  C  C                                       U                                                  ",  # 6  moedas/cogumelo (acima de Q row7)
    "                      Q  Q  Q                                                                                          ",  # 7  Q-blocks tier-2
    "                BBBBBBB                                                                                                 ",  # 8  plataforma tier-2
    "                                C  C  C                                                                                 ",  # 9  moedas acima Q row10
    "                                Q  Q  Q                                                                                 ",  # 10 Q-blocks bativeis do chão
    "                                                                                                                        ",  # 11 céu
    "                                          BBBBBBB                              BBBBBBB                                 ",  # 12 plataformas tier-1
    "                                                                                                                        ",  # 13 céu
    "                                                                                                                        ",  # 14 céu
    "                    P                                   P                                 P                        F   ",  # 15 canos + bandeira
    "     E                              E           E                       E                               E               ",  # 16 inimigos
    "########################################################################################################################################",  # 17 chão
]

# ── Fase 2 — Pedras e Pontes (médio, 140 colunas) ────────────────────────────
# Layout: chão com 3 buracos — é preciso usar as plataformas para cruzar.
# Plataformas:
#   Row 12: BBBBBBB em cols 18-24, 58-64, 102-108  (tier 1 — ponte sobre buracos)
#   Row  8: BBBBBBB em cols 34-40, 78-84            (tier 2 — acesso a Q superiores)
# Blocos-Q:
#   Row 10: Q  Q  Q em cols 24,27,30 e 68,71,74   (bativeis do chão/tier 1)
#   Row  7: Q  Q  Q em cols 38,41,44 e 82,85,88   (bativeis do tier 2)
# Canos: cols 8, 48, 88, 124   Bandeira: col 136
# Buracos: row 17 tem gaps em cols 32-37, 76-81, 118-121
LEVEL_2 = [
    "                                                                                                                                        ",  # 0
    "                                                                                                                                        ",  # 1
    "                                                                                                                                        ",  # 2
    "                                                                                                                                        ",  # 3
    "                             S                                                                                                          ",  # 4  estrela (reward tier-2)
    "                                                                                                                                        ",  # 5
    "                                    C  C  C                                   C  C  C                                                   ",  # 6  moedas acima Q row7
    "                                    Q  Q  Q                                   Q  Q  Q                                                   ",  # 7  Q-blocks tier-2
    "                                  BBBBBBB                                   BBBBBBB                                                     ",  # 8  plataformas tier-2
    "                        C  C  C                            C  C  C                                                                      ",  # 9  moedas acima Q row10
    "                        Q  Q  Q                            Q  Q  Q                                                                      ",  # 10 Q-blocks bativeis do chão
    "                                                                                                                                        ",  # 11 céu
    "                  BBBBBBB                          BBBBBBB                            BBBBBBB                                           ",  # 12 plataformas tier-1 (pontes)
    "                                                                                                                                        ",  # 13 céu
    "                                                                                                                                        ",  # 14 céu
    "        P                                   P                                   P                          P                        F   ",  # 15 canos + bandeira
    " E    E         E   E         E   E                E       E    E                    E      E          E         E                      ",  # 16 inimigos
    "########  ###########  ###########  ###########  ########  #####  ############  ##########  ###########  ##########  ##  ###############",  # 17 chão com buracos
]

# ── Fase 3 — Castelo Vulcânico (difícil, 160 colunas) ────────────────────────
# Layout: chão com 5 buracos largos — plataformas em zigue-zague obrigatório.
# Plataformas:
#   Row 13: BBBBBBB em cols 14-20, 46-52, 86-92, 126-132  (tier 1 — sobre buracos)
#   Row 10: BBBBBBB em cols 28-34, 64-70, 104-110          (tier 2 — salto intermediário)
#   Row  7: BBBBBBB em cols 40-46, 78-84, 118-124          (tier 3 — acesso a Q do topo)
# Blocos-Q:
#   Row 11: Q  Q  Q em cols 18,21,24 e 52,55,58 e 90,93,96  (bativeis do tier 1)
#   Row  8: Q  Q  Q em cols 32,35,38 e 68,71,74             (bativeis do tier 2)
#   Row  5: Q  Q  Q em cols 44,47,50 e 82,85,88             (bativeis do tier 3) + U e S
# Canos: cols 6, 54, 100, 142   Bandeira: col 154
# Buracos: gaps em cols 26-31, 58-65, 98-105, 136-139, 150-153
LEVEL_3 = [
    "                                                                                                                                                        ",  # 0
    "                                                                                                                                                        ",  # 1
    "                                                                                                                                                        ",  # 2
    "                                          C  C  C                                                 C  C  C                                               ",  # 3  moedas acima Q row4
    "                                          Q  Q  Q              U                                  Q  Q  Q              S                               ",  # 4  Q-blocks tier-3 reward
    "                                                                                                                                                        ",  # 5
    "                                C  C  C                                    C  C  C                                                                      ",  # 6  moedas acima Q row7
    "                                Q  Q  Q                                    Q  Q  Q                                                                      ",  # 7  Q-blocks tier-3
    "                              BBBBBBB                                    BBBBBBB                                BBBBBBB                                 ",  # 8  plataformas tier-3
    "                  C  C  C                          C  C  C                              C  C  C                                                          ",  # 9  moedas acima Q row10
    "                  Q  Q  Q                          Q  Q  Q                              Q  Q  Q                                                          ",  # 10 Q-blocks tier-2
    "                BBBBBBB                          BBBBBBB                              BBBBBBB                                                            ",  # 11 plataformas tier-2
    "                                                                                                                                                        ",  # 12 céu
    "              BBBBBBB                          BBBBBBB                              BBBBBBB                          BBBBBBB                            ",  # 13 plataformas tier-1
    "                                                                                                                                                        ",  # 14 céu
    "      P                                                 P                                                P                                    P     F   ",  # 15 canos + bandeira
    "E  E      E E  E   E  E   E  E     E     E   E    E   E    E   E     E   E   E     E  E    E    E   E                  E    E   E   E   E                ",  # 16 muitos inimigos!
    "######  ####  #####  ###  #####  ####  #####  ####  ######  ####  #####  ###  #####  ###  #####  ####  ####  ########  ###  ####  ####  ####  ###########",  # 17 chão c/ buracos largos
]
