from grid import Grid

from blocks import *
import random
import pygame
from colors import *
import os  # To handle file operations for saving the record

class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.paused = False  # New attribute to track pause state
        self.score = 0
        self.level = 1
        self.speed = 500 # Initial speed in milliseconds
        self.GAME_UPDATE = pygame.USEREVENT + 1  # Custom game event
        pygame.time.set_timer(self.GAME_UPDATE, self.speed)

        self.rotate_sound = pygame.mixer.Sound("Sounds/Sounds_rotate.ogg")
        self.clear_sound = pygame.mixer.Sound("Sounds/Sounds_clear.ogg")

        pygame.mixer.music.load("Sounds/Sounds_music.ogg")
        pygame.mixer.music.play(-1)

    def get_record(self):
        """Retrieve the highest score from a file."""
        if not os.path.exists("record.txt"):
            with open("record.txt", "w") as file:
                file.write("0")
        with open("record.txt", "r") as file:
            return int(file.readline())

    def set_record(self):
        """Save the new highest score if it surpasses the current record."""
        current_record = self.get_record()
        if self.score > current_record:
            with open("record.txt", "w") as file:
                file.write(str(self.score))

    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        elif lines_cleared == 4:
            self.score += 700

        self.score += move_down_points

        # Check and update the speed when the score crosses a threshold
        self.update_speed()

    def update_speed(self): 
        # Increase speed when score crosses 200 points or its multiples
        if self.score // 200 > (self.score - 200) // 200:  # Detect new 200-point milestone
            self.speed = max(50, self.speed - 50)  # Reduce delay for faster speed, minimum is 50ms
            pygame.time.set_timer(self.GAME_UPDATE, self.speed)
            print(f"Speed increased! New speed: {self.speed}ms")

    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    def move_left(self):
        self.current_block.move(0, -1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, 1)

    def move_right(self):
        self.current_block.move(0, 1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, -1)

    def move_down(self):
        self.current_block.move(1, 0)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(-1, 0)
            self.lock_block()

    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        if rows_cleared > 0:
            self.clear_sound.play()
            self.update_score(rows_cleared, 0)
        if not self.block_fits():
            self.trigger_game_over()

    def trigger_game_over(self):
        self.set_record()  # Save the record
        self.game_over = True

    def reset(self):
        self.grid.reset()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0
        self.level = 1
        self.speed = 400
        pygame.time.set_timer(self.GAME_UPDATE, self.speed)

    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_empty(tile.row, tile.column):
                return False
        return True

    def rotate(self):
        self.current_block.rotate()
        if not self.block_inside() or not self.block_fits():
            self.current_block.undo_rotation()
        else:
            self.rotate_sound.play()

    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_inside(tile.row, tile.column):
                return False
        return True

    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen, 11, 11)

        if self.next_block.id == 3:
            self.next_block.draw(screen, 255, 290)
        elif self.next_block.id == 4:
            self.next_block.draw(screen, 255, 280)
        else:
            self.next_block.draw(screen, 270, 270)

        
        font = pygame.font.Font(None, 36)
      
        record_text = font.render(f"Record: {self.get_record()}", True, Colors.white)
        record_value = font.render(f"{self.get_record()}", True, Colors.yellow)
        screen.blit(record_text, (345, 130))

    def toggle_pause(self):
        """Toggle the paused state of the game and manage background music."""
        self.paused = not self.paused
        if self.paused:
            pygame.mixer.music.pause()  # Pause background music
        else:
            pygame.mixer.music.unpause()  # Resume background music

    def draw_pause_menu(self, screen):
        """Draw the pause menu on the screen."""
        if self.paused:
            font = pygame.font.Font(None, 74)  # Use any font of your choice
            pause_text = font.render("Paused", True, Colors.active_score_next_text)
            screen.blit(pause_text, (70, 300))  # Adjust position as needed
