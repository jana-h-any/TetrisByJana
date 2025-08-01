import pygame
from game import Game
from colors import Colors

pygame.init()

# Initialize Fonts and Surfaces
title_font = pygame.font.Font(None, 40)
#score_surface = title_font.render("Score", True, Colors.white)
#next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)

# Rectangles for UI elements
score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)

# Setup screen and window title
screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Python Tetris")

clock = pygame.time.Clock()
game = Game()

# Event timers
GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 200)

# Load Sound Icons
sound_on_icon = pygame.image.load('unmute.png')
sound_off_icon = pygame.image.load('mute.png')
mute_button_rect = pygame.Rect(350, 500, sound_on_icon.get_width(), sound_on_icon.get_height())

# Restart Button
restart_button_image = pygame.image.load('restart.png')  
restart_button_rect = restart_button_image.get_rect(center=(440, 525))

# Theme Toggle Button
theme_button_image = pygame.image.load('themes.png') 
theme_button_rect = theme_button_image.get_rect(topleft=(350, 550))  # Position the theme toggle button

# Pause/Play Button
pause_icon = pygame.image.load('pause.png') 
play_icon = pygame.image.load('play.png')   
pause_button_rect = pygame.Rect(420, 550, pause_icon.get_width(), pause_icon.get_height())  # Adjust position

buttons_panel_rect = pygame.Rect(320, 480, 170, 140)  # Adjust dimensions and position as needed

# Variables
is_muted = False
current_theme = "dark"  # Default theme

# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            #sys.exit()
        if event.type == pygame.KEYDOWN:
            if game.game_over:
                game.game_over = False
                game.reset()
            elif not game.paused and not game.game_over:  # Only respond to game controls if not paused
                if event.key == pygame.K_LEFT:
                    game.move_left()
                elif event.key == pygame.K_RIGHT:
                    game.move_right()
                elif event.key == pygame.K_DOWN:
                    game.move_down()
                    game.update_score(0, 1)
                elif event.key == pygame.K_UP:
                    game.rotate()
        if event.type == GAME_UPDATE and not game.paused and not game.game_over:
            game.move_down()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Handle mute button click
            if mute_button_rect.collidepoint(event.pos):
                is_muted = not is_muted
                if is_muted:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            # Handle restart button click
            if restart_button_rect.collidepoint(event.pos):
                game.reset()
                game.game_over = False
            # Handle theme toggle button click
            if theme_button_rect.collidepoint(event.pos):
                current_theme = "light" if current_theme == "dark" else "dark"
            # Handle pause/play button click
            if pause_button_rect.collidepoint(event.pos):
                game.toggle_pause()  # Toggle pause/play state

    # Set active colors based on the current theme
    Colors.set_theme(current_theme)

    # Drawing
    score_value_surface = title_font.render(str(game.score), True, Colors.active_text)

    score_surface = title_font.render("Score", True, Colors.active_score_next_text)
    next_surface = title_font.render("Next", True, Colors.active_score_next_text)

    screen.fill(Colors.active_background)
    screen.blit(score_surface, (365, 20, 50, 50))
    screen.blit(next_surface, (375, 180, 50, 50))

    pygame.draw.rect(screen, Colors.active_score_bg, buttons_panel_rect, 0, 10)  # Rounded rectangle

    if game.game_over:
        screen.blit(game_over_surface, (320, 450, 50, 50))

    pygame.draw.rect(screen, Colors.active_score_bg, score_rect, 0, 10)
    screen.blit(score_value_surface, score_value_surface.get_rect(centerx=score_rect.centerx,
                                                                  centery=score_rect.centery))
    pygame.draw.rect(screen, Colors.active_score_bg, next_rect, 0, 10)
    # pygame.draw.rect(screen, Colors.active_score_bg, buttons_panel_rect, 0, 10)  # Background rectangle for buttons#

    if not game.paused:
        game.draw(screen)  # Draw the game only if not paused
    else:
        game.draw_pause_menu(screen)  # Display the pause menu when paused

    # Draw the mute button with appropriate icon
    if is_muted:
        screen.blit(sound_off_icon, mute_button_rect.topleft)
    else:
        screen.blit(sound_on_icon, mute_button_rect.topleft)

    # Draw the restart button
    screen.blit(restart_button_image, restart_button_rect.topleft)

    # Draw the theme toggle button
    screen.blit(theme_button_image, theme_button_rect.topleft)

    # Draw the pause/play button with the appropriate icon
    if game.paused:
        screen.blit(play_icon, pause_button_rect.topleft)  # Show play icon if paused
    else:
        screen.blit(pause_icon, pause_button_rect.topleft)  # Show pause icon if running

    pygame.display.update()
    clock.tick(60)