import pygame
import os

# Initialize font module
pygame.font.init()

# Game window settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

GRAVITY = 0.4

# Asset paths (ensure work in any environment)
P1_IMG_PATH = os.path.join("images", "player1.png")
P2_IMG_PATH = os.path.join("images", "player2.png")
BALL_IMG_PATH = os.path.join("images", "volleyball_ball.png")
BG_IMG_PATH = os.path.join("images", "background.png")

# Actual display size of game objects (Width, Height)
PLAYER_SIZE = (100, 100)
BALL_SIZE = (50, 50)


# Color definitions
WHITE = (255, 255, 255)
BALL_COLOR = (255, 215, 0)
NET_COLOR = (200, 200, 200)
GROUND_COLOR = (235, 195, 120)
RED = (255, 80, 80)
BLUE = (80, 160, 255)

# Font configurations
FONT = pygame.font.SysFont("Arial", 40)
LARGE_FONT = pygame.font.SysFont("Arial", 60)