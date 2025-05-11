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

def create_grid(rows=14, cols=14):
    """
    line = lambda r, c: ('+' if r % 2 == 0 and c % 2 == 0 else '---' if r % 2 == 0 else '|' if c % 2 == 0 else '   ')
    
    grid = [[line(r, c) for c in range(cols * 2 + 1)]for r in range(rows * 2 + 1)]
    
    return grid
    """
    
    
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

def change_plus(grid, row, col, new_char):
    
    # Convert 1-based user input into actual grid indices (2x spacing)
    r = (row - 1) * 2
    c = (col - 1) * 2
    # Validate the location and ensure it's a '+'
    if 0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c] == '+':
        grid[r][c] = new_char  # Replace the '+' with the player's character
        print(f"✅ Changed '+' at ({row}, {col}) to '{new_char}'")
        return r, c  # Return grid indices for win checking
    else:
        print(f"❗ No '+' found at that position.")
        return None, None  # Invalid move
    
   
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
def check_win(grid, r, c, target_char, length=5):
    # Helper to count matching characters in a direction
    

    # Directions to check: (down, right), (diagonal \), (diagonal /)
    directions = [
        (0, 2),    # Horizontal (left-right)
        (2, 0),    # Vertical (up-down)
        (2, 2),    # Diagonal \
        (2, -2),   # Diagonal /
    ]

    # For each direction, check both forward and backward counts
    for dr, dc in directions:
        total = 1  # Start with the placed marker
        total += count_direction(grid,dr, dc,r,c,target_char)       # Count forward
        total += count_direction(grid,-dr, -dc,r,c,target_char)     # Count backward
        if total >= length:
            print(f"\n🎉 Player wins with {length} in a row!")
            return True  # Win detected
    return False  # No win yet

def choose_player_colour():
    playerInput = input("do you wish to play as Black (1st) or White (2nd) (B/W): ")
    whitelist = ['b','w','B','W']
    if(playerInput in whitelist):
        if(playerInput.capitalize() == 'B'):
            return playerInput.capitalize()
    else:
        print("Please type B or W")
        choose_player_colour()
    
    

def main():
    player1: str = ""
    
    playerColour = choose_player_colour()
    grid = create_grid()  # Initialize the grid
    
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
            r, c = change_plus(grid, row, col, new_char)  # Place move
            if r is not None:
                if check_win(grid, r, c, new_char):  # Check for a win
                    print_grid(grid)
                    break  # End game on win
        except ValueError:
            print("Invalid input. Use numbers for coordinates.")
        except KeyboardInterrupt:
            print("\nExiting.")  # Exit cleanly on Ctrl+C
            break

if __name__ == "__main__":
    print(programIntroduction)
    main()  # Start the game
