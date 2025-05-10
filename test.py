# -*- coding: utf-8 -*-
"""
Created on Sat May 10 14:16:21 2025

@author: henrikas
"""
"""
def create_grid(rows=16, cols=16):
    grid = []
    for r in range(rows * 2 + 1):
        line = []
        for c in range(cols * 2 + 1):
            if r % 2 == 0:
                if c % 2 == 0:
                    line.append('+')
                else:
                    line.append('---')
            else:
                if c % 2 == 0:
                    line.append('|')
                else:
                    line.append('   ')
        grid.append(line)
    return grid

def print_grid(grid):
    num_cols = (len(grid[0]) + 1) // 2
    print("     ", end="")
    for col in range(1, num_cols + 1):
        print(f"{col:>4}", end="")
    print()
    for r_idx, row in enumerate(grid):
        if r_idx % 2 == 0:
            label = f"{r_idx // 2 + 1:>2}  "
        else:
            label = "    "
        print(label + "".join(row))

def change_plus(grid, row, col, new_char):
    r = (row - 1) * 2
    c = (col - 1) * 2
    if 0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c] == '+':
        grid[r][c] = new_char
        print(f"✅ Changed '+' at ({row}, {col}) to '{new_char}'")
        return r, c  # return actual grid position
    else:
        print(f"❗ No '+' found at that position.")
        return None, None

def check_win(grid, r, c, target_char, length=5):
    def count_direction(dr, dc):
        count = 0
        i = 1
        while True:
            nr, nc = r + dr * i, c + dc * i
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] == target_char:
                count += 1
                i += 1
            else:
                break
        return count

    directions = [
        (0, 2),    # horizontal right
        (2, 0),    # vertical down
        (2, 2),    # diagonal \
        (2, -2),   # diagonal /
    ]

    for dr, dc in directions:
        total = 1
        total += count_direction(dr, dc)
        total += count_direction(-dr, -dc)
        if total >= length:
            print(f"\n🎉 Player wins with {length} in a row!")
            return True
    return False

def main():
    grid = create_grid()
    while True:
        print_grid(grid)
        try:
            row = int(input("Enter row (1–16) to change '+': "))
            col = int(input("Enter col (1–16) to change '+': "))
            if not (1 <= row <= 16 and 1 <= col <= 16):
                print("❗ Out of range. Try again.")
                continue
            new_char = input("Enter new character to replace '+': ")
            if len(new_char) != 1:
                print("❗ Enter a single character only.")
                continue
            r, c = change_plus(grid, row, col, new_char)
            if r is not None:
                if check_win(grid, r, c, new_char):
                    print_grid(grid)
                    break
        except ValueError:
            print("❗ Invalid input. Use numbers for coordinates.")
        except KeyboardInterrupt:
            print("\n👋 Exiting.")
            break

if __name__ == "__main__":
    main()
"""

def create_grid(rows=14, cols=14):
    """
    grid = []  # Initialize the grid as a list of rows
    for r in range(rows * 2 + 1):  # Loop through total row lines (grid + separators)
        line = []
        for c in range(cols * 2 + 1):  # Loop through total column positions
            if r % 2 == 0:  # Even rows: contain '+' and '---'
                if c % 2 == 0:
                    line.append('+')  # Grid intersection
                else:
                    line.append('---')  # Horizontal edge
            else:  # Odd rows: contain '|' and spaces
                if c % 2 == 0:
                    line.append('|')  # Vertical edge
                else:
                    line.append('   ')  # Empty cell
        grid.append(line)  # Add completed row to grid
    return grid  # Return the entire grid structure
    """
    block = lambda r, c: ('+' if r % 2 == 0 and c % 2 == 0 else '---' if r % 2 == 0 else '|' if c % 2 == 0 else '   ')
    
    grid = [[block(r, c) for c in range(cols * 2 + 1)]for r in range(rows * 2 + 1)]
    return grid

def print_grid(grid):
    """
    num_cols = (len(grid[0]) + 1) // 2  # Calculate number of columns based on grid width
    print("     ", end="")  # Initial spacing for column header
    for col in range(1, num_cols + 1):
        print(f"{col:>4}", end="")  # Print column headers (1 to N), right-aligned
    print()
    for r_idx, row in enumerate(grid):
        if r_idx % 2 == 0:
            label = f"{r_idx // 2 + 1:>2}  "  # Row headers on grid lines
        else:
            label = "    "  # No row header on cell lines
        print(label + "".join(row))  # Print the full row with its label
    """
    columnHeader = lambda grid: (print("   " + "  ".join([f"{col:>2}" for col in range(1, (len(grid[0]) + 1) // 2 + 1)])))
    columnHeader(grid)
    
    
    printRows = lambda grid: list(map(lambda t: print((f"{t[0] // 2 + 1:>2}  " if t[0] % 2 == 0 else "    ") + "".join(t[1])), enumerate(grid)))
    printRows(grid)
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
    
    """
    r, c = (row - 1) * 2, (col - 1) * 2
    return (
        (grid.__setitem__(r, grid[r][:c] + [new_char] + grid[r][c+1:]),
         print(f"✅ Changed '+' at ({row}, {col}) to '{new_char}'"),
         (r, c))[-1]
        if 0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c] == '+'
        else (print("❗ No '+' found at that position."), None)[1]
    )
    """
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

def main():
    grid = create_grid()  # Initialize the grid
    while True:
        print_grid(grid)  # Show the current grid state
        try:
            # Get row and column input from user
            row = int(input("Enter row (1–16) to change '+': "))
            col = int(input("Enter col (1–16) to change '+': "))
            if not (1 <= row <= 16 and 1 <= col <= 16):
                print("❗ Out of range. Try again.")
                continue
            new_char = input("Enter new character to replace '+': ")
            if len(new_char) != 1:
                print("❗ Enter a single character only.")
                continue
            r, c = change_plus(grid, row, col, new_char)  # Place move
            if r is not None:
                if check_win(grid, r, c, new_char):  # Check for a win
                    print_grid(grid)
                    break  # End game on win
        except ValueError:
            print("❗ Invalid input. Use numbers for coordinates.")
        except KeyboardInterrupt:
            print("\n👋 Exiting.")  # Exit cleanly on Ctrl+C
            break

if __name__ == "__main__":
    main()  # Start the game
