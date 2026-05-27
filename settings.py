# ── Tela ──────────────────────────────────────────────────────────────────────
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
FPS           = 60
TITLE         = "Super Python"

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
PLAYER_SPEED         = 4
PLAYER_JUMP_POWER    = -16
PLAYER_GRAVITY       = 0.8
PLAYER_MAX_FALL      = 14
PLAYER_WIDTH         = 32
PLAYER_HEIGHT        = 48
PLAYER_LIVES         = 3
PLAYER_INVINCIBILITY = 120   # frames (2 s a 60 fps)

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
