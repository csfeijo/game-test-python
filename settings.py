# ── Tela ──────────────────────────────────────────────────────────────────────
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
FPS           = 60
TITLE         = "SUPER THÉO"

# ── Cores ─────────────────────────────────────────────────────────────────────
WHITE    = (255, 255, 255)
BLACK    = (0,   0,   0)
RED      = (200, 30,  30)
GREEN    = (34,  139, 34)
BLUE     = (30,  80,  220)
YELLOW   = (255, 220, 0)
ORANGE   = (255, 120, 30)
BROWN    = (139, 90,  43)
SKY_BLUE = (107, 140, 255)
GRAY     = (120, 120, 120)

# ── Jogador ───────────────────────────────────────────────────────────────────
PLAYER_WIDTH         = 32
PLAYER_HEIGHT        = 48
PLAYER_LIVES         = 3
PLAYER_INVINCIBILITY = 120    # frames (2 s a 60 fps)

# Movimento horizontal
PLAYER_ACCEL         = 0.9    # aceleração por frame no chão
PLAYER_AIR_CONTROL   = 0.55   # fator de aceleração no ar
PLAYER_FRICTION      = 0.76   # desaceleração ao soltar tecla (multiplicador/frame)
PLAYER_MAX_SPEED     = 5.5    # velocidade horizontal máxima (px/frame)

# Pulo
PLAYER_JUMP_POWER    = -15.0  # velocidade inicial do pulo
PLAYER_JUMP_CUT      = 0.38   # multiplicador ao soltar cedo (pulo baixo)

# Gravidade assimétrica (arco estilo Mario)
PLAYER_GRAVITY       = 0.60   # gravidade subindo
PLAYER_FALL_GRAVITY  = 1.10   # gravidade caindo (descida mais rápida)
PLAYER_MAX_FALL      = 15.0   # velocidade máxima de queda

# ── Pontuação ─────────────────────────────────────────────────────────────────
SCORE_COIN         = 100
SCORE_ENEMY        = 200
SCORE_POWERUP      = 500
SCORE_TIME_FACTOR  = 10      # multiplicado pelo tempo restante no fim de fase

# ── Inimigo ───────────────────────────────────────────────────────────────────
ENEMY_SPEED  = 1.5
ENEMY_WIDTH  = 32
ENEMY_HEIGHT = 32

# ── Mundo ─────────────────────────────────────────────────────────────────────
TILE_SIZE = 32

# ── Estados do jogo ───────────────────────────────────────────────────────────
STATE_MENU           = "menu"
STATE_PLAYING        = "playing"
STATE_PAUSED         = "paused"
STATE_GAME_OVER      = "game_over"
STATE_LEVEL_COMPLETE = "level_complete"
