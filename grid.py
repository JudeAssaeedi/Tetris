from colors import Colors
import pygame

class Grid:
    def __init__(self): #whenever u want to def a class u put this line
        self.num_rows = 20
        self.num_cols = 11
        self.cell_size = 30
        self.grid = [[0 for j in range(self.num_cols)]for i in range(self.num_rows)] #filling grid with 0s
        self.colors = Colors.get_cell_colors()
        self.clear_animation_active = False  # To track if an animation is ongoing
        self.clear_animation_cells = []  # Cells being cleared
        self.clear_row_index = 0  # To track current index in the animation
        self.clear_animation_speed = 20  # Time between each block removal (customizable)
        self.row_to_clear = None  # Row to be cleared (set when a full row is detected)
        self.rows_to_clear = []  # List of rows that need clearing

    # Function to trigger row-clearing animation
    def animate_clear_row(self, row):
        mid = self.num_cols // 2  # Find the middle of the row
        # Build a list of columns to be cleared, starting from the middle
        self.clear_animation_cells = [mid]
        for i in range(1, mid + 1):
            if mid - i >= 0: self.clear_animation_cells.append(mid - i)
            if mid + i < self.num_cols: self.clear_animation_cells.append(mid + i)
        
        self.clear_row_index = 0  # Reset the index
        self.clear_animation_active = True  # Activate the animation
        self.row_to_clear = row  # Set the row to clear

        # Set a timer to control the animation
        pygame.time.set_timer(pygame.USEREVENT + 1, self.clear_animation_speed)


    # method (update_clear_animation)
    def update_clear_animation(self, row):

        if self.clear_animation_active and self.clear_row_index < len(self.clear_animation_cells):
            col = self.clear_animation_cells[self.clear_row_index]
            self.grid[self.row_to_clear][col] = 0  # Clear the block
            self.clear_row_index += 1
        else:
            # End the animation once all blocks are cleared
            self.clear_animation_active = False
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # Stop the timer

            # Move rows down right after clearing the row
            self.move_rows_down_after_clear(self.row_to_clear)

            # If there are more rows to clear, animate the next row
            if self.rows_to_clear:
                self.animate_clear_row(self.rows_to_clear.pop(0))


    def move_rows_down_after_clear(self, cleared_row):
        """Move all rows above the cleared row down by 1."""
        
        # Move rows above the cleared one down
        for row in range(cleared_row, 0, -1):
            for col in range(self.num_cols):
                self.grid[row][col] = self.grid[row - 1][col]
        
        # Clear the top row (row 0) after shifting
        for col in range(self.num_cols):
            self.grid[0][col] = 0

        # Check again for full rows after moving down
        self.rows_to_clear = self.check_full_rows()
        
        if self.rows_to_clear:
            next_row = self.rows_to_clear.pop(0)
            self.animate_clear_row(next_row)



    def print_grid(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                print(self.grid[row][column], end = "")
            print() #new line

    def is_inside(self, row, column):
        if row >= 0 and row < self.num_rows and column >= 0 and column < self.num_cols:
            return True
        return False
    
    def is_empty(self, row, column):
        if self.grid[row][column] == 0:
            return True
        return False
    
    def is_row_full(self, row):
        for column in range(self.num_cols):
            if self.grid[row][column] == 0:
                return False
        return True
    
    def clear_row(self, row):
       self.animate_clear_row(row)


    # the method (move_row_down)
    def move_row_down(self, row, num_rows):
        for r in range(row, 0, -1):
            for column in range(self.num_cols):
                self.grid[r][column] = self.grid[r - num_rows][column]  # Move the row down
        for column in range(self.num_cols):
            self.grid[0][column] = 0  # Clear the top row


    def clear_full_row(self):
        rows_to_clear = []  # Initialize an empty list to store rows that need to be cleared
        
        # Check each row for fullness
        for row in range(self.num_rows):  # Iterate over each row in the grid
            if all(self.grid[row]):  # Check if all columns in the current row are filled
                # print(f"Row {row} is full and will be cleared.")  # Log the full row
                rows_to_clear.append(row)  # If filled, add the row index to the list

        # If rows are found, animate the first row
        if rows_to_clear:
            self.rows_to_clear = rows_to_clear  # Store the rows that need to be cleared
            self.animate_clear_row(rows_to_clear[0])  # Start the animation for the first row

        return rows_to_clear  # Return the list of cleared rows


    def check_full_rows(self):
        """Check for full rows and return a list of row indices that are full."""
        full_rows = []
        for row in range(self.num_rows):
            if all(self.grid[row][col] != 0 for col in range(self.num_cols)):
                full_rows.append(row)
        return full_rows

    
    def reset(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                self.grid[row][column] = 0

    def draw(self, screen): #to draw the block on the screen
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                cell_value = self.grid[row][column]
                cell_rect = pygame.Rect(column * self.cell_size +11, row * self.cell_size +11, self.cell_size -1, self.cell_size -1)
                pygame.draw.rect(screen, self.colors[cell_value], cell_rect)