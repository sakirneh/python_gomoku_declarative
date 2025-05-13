# -*- coding: utf-8 -*-
"""
Created on Sat May 10 14:16:21 2025

@author: henrikas
"""

programIntroduction : str = """
Gomoku game
By Henrikas Varanauskas
ID 23178823
2025

"""

def create_grid():
    rows: int=14 
    cols: int=14
    symbols = {
        (0, 0): '+',     # intersection
        (0, 1): '---',   # horizontal line
        (1, 0): '|',     # vertical line
        (1, 1): '   ',   # empty cell
    }

    cell_char = lambda r, c: symbols[(r % 2, c % 2)]

    grid = [[cell_char(r, c) for c in range(cols * 2 +1)]for r in range(rows * 2 +1)]
    
    return grid

def print_grid(grid):
    
    columnHeader = lambda grid: (print("   " + "  ".join([f"{col:>2}" for col in range(1, (len(grid[0]) + 1) // 2 + 1)])))
    
    printRows = lambda grid: list(map(lambda x: print((f"{x[0] // 2 + 1:>2}  " if x[0] % 2 == 0 else "    ") + "".join(x[1])), enumerate(grid)))
    
    return columnHeader(grid),printRows(grid)

def get_grid_index(row, col):
    """Convert user-facing 1-based coordinates to grid indices."""
    return (row - 1) * 2, (col - 1) * 2

def is_valid_position(grid, r, c):
    """Check if the position is within bounds and has a '+'."""
    return (0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c] == '+')

def update_grid(grid, r, c, new_char):
    """Replace the '+' at position (r, c) with the new character."""
    return grid[r][:c] + [new_char] + grid[r][c + 1:]

def place_stone(grid, row, col, new_char):
    """Wrapper to handle user input and modify grid if valid."""
    r, c = get_grid_index(row, col)
    if is_valid_position(grid, r, c):
        grid[r] = update_grid(grid, r, c, new_char)
        print(f"")
        return r, c
    else:
        print("Not a valid placement")
        

    
   
def count_direction(grid,dr, dc,r,c, target_char):
    count = 0
    i = 1
    while True:
        nr, nc = r + dr * i, c + dc * i  # Move in the given direction
        # Stop if out of bounds or character mismatch
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] == target_char:
            count += 1
            i += 1
        else:
            break
    return count
def check_win(grid, r, c, players):
    # Helper to count matching characters in a direction
    

    # Directions to check: (down, right), (diagonal \), (diagonal /)
    directions = [
        (0, 2),    # Horizontal (left-right)
        (2, 0),    # Vertical (up-down)
        (2, 2),    # Diagonal \
        (2, -2),   # Diagonal /
    ]

    # For each direction, check both forward and backward counts
    for dRow, dColumn in directions:
        total = 1  # Start with the placed marker
        total += count_direction(grid,dRow, dColumn,r,c,players)       # Count forward
        total += count_direction(grid,-dRow, -dColumn,r,c,players)     # Count backward
        if total >= 5:
            print(f"\n Player wins with 5 in a row!")
            return True  # Win detected
    return False  # No win yet

def choose_player_colour():
    """Ask Player 1 to choose 'B' or 'W', assign the other to Player 2."""
    valid_choices = {'B', 'W'}
    while True:
        choice = input("Player 1, do you want to be Black (B) or White (W)? ").upper()
        if choice in valid_choices:
            player1 = choice
            player2 = (valid_choices - {choice}).pop()  # Get the other symbol
            print(f" Player 1 is '{player1}', Player 2 is '{player2}'")
            return player1, player2
        else:
            print(" Invalid choice. Please enter 'B' or 'W'.")

    

def main():
    
    players = choose_player_colour()
    grid = create_grid()  # Initialize the grid
    print(players)
    while True:
        print_grid(grid)  # Show the current grid state
        try:
            # Get row and column input from user
            row = int(input("Enter row (1–15) to change '+': "))
            col = int(input("Enter col (1–15) to change '+': "))
            if not (1 <= row <= 15 and 1 <= col <= 15):
                print(" Out of range. Try again.")
                continue
            new_char = input("Enter new character to replace '+': ")
            if len(new_char) != 1:
                print("Enter a single character only.")
                continue
            r,c = place_stone(grid, row, col, new_char)
            break  # End game on win
        except ValueError:
            print("Invalid input. Use numbers for coordinates.")
        except KeyboardInterrupt:
            print("\nExiting.")  # Exit cleanly on Ctrl+C
            break

if __name__ == "__main__":
    print(programIntroduction)
    main()  # Start the game
