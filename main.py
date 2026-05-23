import pygame
import sys
import os
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BG_IMG_PATH
from player import Player
from ball import Ball
from game_view import draw_game_scene

# ==============================================================================
# Game Entry Point: Initializes systems, loads assets, and starts the game loop.
# ==============================================================================
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pixel Beach Smash")
    clock = pygame.time.Clock()

    # Load background image if available
    if os.path.exists(BG_IMG_PATH):
        raw_img = pygame.image.load(BG_IMG_PATH).convert()
        bg_image = pygame.transform.scale(raw_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    else:
        bg_image = None

    
    # Create game objects
    player1 = Player(200, 500, is_p1=True)
    player2 = Player(600, 500, is_p1=False)
    ball = Ball()

    winner = None 
    running = True
    
    while running:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()
        
        # Event Listening Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Restarting the game with SPACE bar
            if winner is not None and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player1.score = 0
                    player2.score = 0
                    player1.x, player1.y = 200, 500
                    player2.x, player2.y = 600, 500
                    ball.reset(1)
                    winner = None

        # Proceed with normal gameplay updates if there is no winner yet
        if winner is None:
            # Move Players
            player1.move(keys)
            player2.move(keys)

            # Update Ball
            ball.update()
            ball.check_collision_player(player1, keys)
            ball.check_collision_player(player2, keys)
            ball.check_collision_net()

            # Score Detection & Round Reset
            if ball.y >= SCREEN_HEIGHT - 50 - ball.radius:
                if ball.x < SCREEN_WIDTH // 2:
                    player2.score += 1
                    ball.reset(1) # Player 1 serves next round
                else:
                    player1.score += 1
                    ball.reset(2) # Player 2 serves next round
                
                # Reset player starting positions for the new round
                player1.x, player1.y = 200, 500
                player2.x, player2.y = 600, 500

            # Check Match Winning Conditions (First to 10 points)
            if player1.score >= 10:
                winner = "Player 1"
            elif player2.score >= 10:
                winner = "Player 2"

        # Render the Scene
        draw_game_scene(screen, player1, player2, ball, winner, bg_image)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()