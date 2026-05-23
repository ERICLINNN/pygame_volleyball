import pygame
import math
import os
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY, BALL_IMG_PATH, BALL_SIZE

class Ball:
    def __init__(self):
        self.radius = BALL_SIZE[0] // 2
        self.delay_timer = 0  # for 1 second delay at the start of each round
        self.reset(1)

        if not os.path.exists(BALL_IMG_PATH):
            print(f"ERROR: Can not found Volleyball Image {BALL_IMG_PATH}")
            pygame.quit()
            import sys
            sys.exit()
        
        self.original_image = pygame.image.load(BALL_IMG_PATH).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, BALL_SIZE)

        

    def reset(self, server):
        self.y = 200
        self.vel_y = 0
        self.delay_timer = 60  # 1 second pause (60 frames at 60 FPS)
        
        if server == 1:
            self.x = 200
            self.vel_x = 1
        else:
            self.x = 600
            self.vel_x = -1

    def update(self):
        # If the start-of-round delay timer is active, freeze the ball
        if self.delay_timer > 0:
            self.delay_timer -= 1
            return 

        # Timer expired: Apply gravity and update physics position
        self.vel_y += GRAVITY
        self.x += self.vel_x
        self.y += self.vel_y

        # Left and right wall bounce collision handling
        if self.x < self.radius:
            self.x = self.radius
            self.vel_x *= -1
        if self.x > SCREEN_WIDTH - self.radius:
            self.x = SCREEN_WIDTH - self.radius
            self.vel_x *= -1

    def check_collision_player(self, player, keys):
        # Skip collision checks if the ball is still frozen at the start of a round
        if self.delay_timer > 0:
            return

        dx = self.x - player.x
        dy = self.y - player.y
        distance = math.hypot(dx, dy)

        # Check if the ball is touching
        if distance < self.radius + player.radius:
            is_smashing = False
            
            # P1 Smash conditions: character is mid-air and presses G
            if player.is_p1 and keys[pygame.K_g] and player.is_jumping:
                is_smashing = True
            # P2 Smash conditions: character is mid-air and presses Enter
            elif not player.is_p1 and (keys[pygame.K_RETURN] or keys[pygame.K_KP_ENTER]) and player.is_jumping:
                is_smashing = True
            # ----------------------------

            if is_smashing:
                self.vel_x = 18 if player.is_p1 else -18     
                self.vel_y = -1  
                self.x += 15 if player.is_p1 else -15

            else:
                # Standard bounce physics
                angle = math.atan2(dy, dx)
                self.vel_x = math.cos(angle) * 12
                self.vel_y = math.sin(angle) * 12
                if self.vel_y > -4: 
                    self.vel_y = -8

    def check_collision_net(self):
        net_x = SCREEN_WIDTH // 2
        net_top = SCREEN_HEIGHT - 230 

        if net_top <= self.y <= SCREEN_HEIGHT - 50:
            if abs(self.x - net_x) < self.radius + 10:
                self.vel_x *= -1
                
                # Reposition the ball to prevent it from getting stuck inside the net
                if self.x < net_x:
                    self.x = net_x - 11 - self.radius
                else:
                    self.x = net_x + 11 + self.radius

    def draw(self, surface):
        top_left_x = self.x - self.radius
        top_left_y = self.y - self.radius
        surface.blit(self.image, (int(top_left_x), int(top_left_y)))