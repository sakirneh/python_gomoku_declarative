# -*- coding: utf-8 -*-
"""
Created on Sat May 10 16:17:34 2025

@author: henrikas
"""

def create_grid():
    rows: int=14
    cols: int=14
    
    block = lambda r, c: ('+' if r % 2 == 0 and c % 2 == 0 else '---' if r % 2 == 0 else '|' if c % 2 == 0 else '   ')
    
    return [[block(r, c) for c in range(cols * 2 + 1)]for r in range(rows * 2 + 1)]

def print_grid(grid):
    
    columnHeader = lambda grid: (print("   " + "  ".join([f"{col:>2}" for col in range(1, (len(grid[0]) + 1) // 2 + 1)])))
    columnHeader(grid)
    
    
    printRows = lambda grid: list(map(lambda t: print((f"{t[0] // 2 + 1:>2}  " if t[0] % 2 == 0 else "    ") + "".join(t[1])), enumerate(grid)))
    printRows(grid)
   
    
        
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
           
        except ValueError:
            print("❗ Invalid input. Use numbers for coordinates.")
        except KeyboardInterrupt:
            print("\n👋 Exiting.")  # Exit cleanly on Ctrl+C
            break

if __name__ == "__main__":
    main()  # Start the game