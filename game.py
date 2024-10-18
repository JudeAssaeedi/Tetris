from grid import Grid
from blocks import *
from block import *
from constants import GAME_UPDATE
import random

#100 points for a single line clear
#300 ponits for a double line clear
#500 points for a triple line clear
#5 point for each move down by the player

class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [LBlock(), JBlock(), IBlock(), OBlock(), oBlock(), SBlock(), TBlock(), tBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
        self.animation_in_progress = False  # Initialize the flag
        
    def update_score(self, lines_cleared, move_down_points): #lscore += lines cleared * 100 
        self.score += lines_cleared * 100
        self.score += move_down_points

    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [LBlock(), JBlock(), IBlock(), OBlock(), oBlock(), SBlock(), TBlock(), tBlock(), ZBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block
    
    def move_left(self):
        self.current_block.move(0, -1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, 1)
    
    def move_right(self):
        self.current_block.move(0, 1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, -1)

    def move_down(self, screen):
        self.current_block.move(1, 0)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(-1, 0)
            self.lock_block(screen)
            pygame.time.set_timer(GAME_UPDATE, 300)

    def animate_row_clear(self, screen, rows_to_clear):
        # This method will handle the animation for row clearing.
        # 'rows_to_clear' contains the list of rows that need to be cleared.

        # You can customize this animation loop based on your needs.
        animation_speed = 100  # Customize the speed of the animation

        for row in rows_to_clear:
            for col in range(self.grid.num_cols):
                # Here we make the blocks disappear from the middle block by block
                mid_col = self.grid.num_cols // 2

                for offset in range(mid_col + 1):
                    if mid_col - offset >= 0:
                        # Clear the left side block by block
                        self.grid.grid[row][mid_col - offset] = 0
                    if mid_col + offset < self.grid.num_cols:
                        # Clear the right side block by block
                        self.grid.grid[row][mid_col + offset] = 0

                    # Redraw the screen to show the animation step
                    self.draw(screen)  # Assuming draw method will redraw the grid and blocks
                    pygame.display.update()

                    # Control the speed of the animation
                    pygame.time.wait(animation_speed)

        # After the animation is done, clear the rows from the grid
        self.grid.clear_row(rows_to_clear)


    def lock_block(self, screen):

        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id

        # Switch to the next block
        self.current_block = self.next_block
        self.next_block = self.get_random_block()

        # Clear full rows and trigger animation if necessary
        rows_to_clear = self.grid.clear_full_row()  # Get rows to clear
        
        if rows_to_clear:
            self.grid.rows_to_clear = rows_to_clear  # Store the rows for animation
            self.grid.animate_clear_row(rows_to_clear[0])  # Start animation for the first row
            self.update_score(len(rows_to_clear), 0)  # Update score based on cleared rows
        else:
            # Check if the next block fits only if no rows were cleared
            if not self.block_fits():
                self.game_over = True


    def reset(self):
        self.grid.reset()
        self.blocks = [LBlock(), JBlock(), IBlock(), OBlock(), oBlock(), SBlock(), TBlock(), tBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0

    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_empty(tile.row, tile.column) == False:
                return False
        return True

    def rotate(self):
        self.current_block.rotate()
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.undo_rotation()
        #else:
         #   self.rotate_sound.play()

    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.column) == False:
                return False
        return True #this return statemant was a tab in so it was inside the loop which caused a logical error that mad the loop check for one tile only so pay attention to that


    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen, 11, 11)

        if self.next_block.id == 3:
            self.next_block.draw(screen, 255, 290)
        elif self.next_block.id == 4:
            self.next_block.draw(screen, 255, 280)
        else:
            self.next_block.draw(screen, 270, 270)