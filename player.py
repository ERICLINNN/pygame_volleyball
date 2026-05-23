import pygame
import os
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY, PLAYER_SIZE, P1_IMG_PATH, P2_IMG_PATH

class Player:
    def __init__(self, x, y, is_p1):
        self.is_p1 = is_p1
        self.speed = 6
        self.vel_y = 0
        self.is_jumping = False
        self.score = 0
        
        # Load player image
        img_path = P1_IMG_PATH if self.is_p1 else P2_IMG_PATH
        if not os.path.exists(img_path):
            print(f"ERROR: Cannot find player image file {img_path}")
            pygame.quit()
            import sys
            sys.exit()

        self.original_image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, PLAYER_SIZE)
        
        # (x, y) to represent the "center point" of the character
        self.x = x
        self.y = y
        
        # Get image dimensions for boundary and collision calculations
        self.width = PLAYER_SIZE[0]
        self.height = PLAYER_SIZE[1]
        
        # Collision radius for ball interaction
        self.radius = max(PLAYER_SIZE) // 2

    def move(self, keys):
        # Movement controls and boundary limits
        half_w = self.width // 2
        
        if self.is_p1:
            if keys[pygame.K_a]:
                self.x -= self.speed
            if keys[pygame.K_d]:
                self.x += self.speed
            
            # Restrict P1 to the left side of the court
            if self.x - half_w < 0: 
                self.x = half_w
            if self.x + half_w > SCREEN_WIDTH // 2 - 10: 
                self.x = SCREEN_WIDTH // 2 - 10 - half_w
            
            # Jump
            if keys[pygame.K_w] and not self.is_jumping:
                self.vel_y = -13
                self.is_jumping = True
        else:
            if keys[pygame.K_LEFT]:
                self.x -= self.speed
            if keys[pygame.K_RIGHT]:
                self.x += self.speed
                
            # Restrict P2 to the right side of the court
            if self.x - half_w < SCREEN_WIDTH // 2 + 10: 
                self.x = SCREEN_WIDTH // 2 + 10 + half_w
            if self.x + half_w > SCREEN_WIDTH: 
                self.x = SCREEN_WIDTH - half_w
            
            # Jump
            if keys[pygame.K_UP] and not self.is_jumping:
                self.vel_y = -13
                self.is_jumping = True

        # Gravity simulation
        self.vel_y += GRAVITY
        self.y += self.vel_y

        # Ground collision limits
        half_h = self.height // 2
        if self.y + half_h >= SCREEN_HEIGHT - 50:
            self.y = SCREEN_HEIGHT - 50 - half_h
            self.vel_y = 0
            self.is_jumping = False

    def draw(self, surface):
        # Convert the "center point (x, y)" to "top-left corner coordinates" required by pygame.blit
        top_left_x = self.x - (self.width // 2)
        top_left_y = self.y - (self.height // 2)
        
        surface.blit(self.image, (int(top_left_x), int(top_left_y)))