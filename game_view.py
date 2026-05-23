import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_COLOR, NET_COLOR, WHITE, FONT, LARGE_FONT, RED, BLUE


def draw_game_scene(screen, player1, player2, ball, winner, bg_image):
    # Draw background (if available) or fill with solid color
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill((50, 50, 50))

    # Draw the ground
    pygame.draw.rect(screen, GROUND_COLOR, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
    
    # # Draw the volleyball net
    pygame.draw.rect(screen, NET_COLOR, (SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT - 230, 20, 180))

    # Draw player and ball
    player1.draw(screen)
    player2.draw(screen)
    ball.draw(screen)

    # Display scores
    p1_score_text = FONT.render(str(player1.score), True, WHITE)
    p2_score_text = FONT.render(str(player2.score), True, WHITE)
    screen.blit(p1_score_text, (SCREEN_WIDTH // 4, 50))
    screen.blit(p2_score_text, (3 * SCREEN_WIDTH // 4, 50))

    # Display the "GET READY!"
    if ball.delay_timer > 0 and winner is None:
        ready_text = LARGE_FONT.render("GET READY!", True, WHITE)
        text_rect = ready_text.get_rect(center=(SCREEN_WIDTH // 2, 120))
        screen.blit(ready_text, text_rect)

    # Display the final winner
    if winner is not None:
        win_color = BLUE if winner == "Player 1" else RED
        win_text = LARGE_FONT.render(f"{winner} WINS!", True, win_color)
        text_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        
        restart_text = FONT.render("Press SPACE to Restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        
        screen.blit(win_text, text_rect)
        screen.blit(restart_text, restart_rect)