# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import TypeAlias

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
    if grid[r][c] == '+':
        return (grid[r][c] == '+')
    else:
        return False

def update_grid(grid, r, c, stone):
    """Replace the '+' at position (r, c) with the new character."""
    return grid[r][:c] + [stone] + grid[r][c + 1:]

def place_stone(grid, row, col, stone):
    
    r, c = get_grid_index(row, col)
    if is_valid_position(grid, r, c):
        grid[r] = update_grid(grid, r, c, stone)
        
        return r, c
    
        
def count_in_direction(grid, r, c, dr, dc, targetChar, i=1):
    nr, nc = r + dr * i, c + dc * i

    if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] == targetChar:
        return 1 + count_in_direction(grid, r, c, dr, dc, targetChar, i + 1)
    else:
        return 0
        
def count_direction(grid,dr, dc,r,c, target_char):
    count = count_in_direction(grid, r, c, dr, dc, target_char)
    return count
def check_win(grid, r, c, currStone):
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
        total += count_direction(grid,dRow, dColumn,r,c,currStone)       # Count forward
        total += count_direction(grid,-dRow, -dColumn,r,c,currStone)     # Count backward
        if total >= 5:
            print(f"\n Player wins with 5 in a row!")
            return True  # Win detected
    return False  # No win yet

def choose_players_colours():
    """Ask Player 1 to choose 'B' or 'W', assign the other to Player 2."""
    colourChoice = ['B','W']
    
    choice = input("Player 1, do you want to be Black (B) or White (W)? ").upper()
    assign_players = lambda choice: colourChoice if choice == 'B' else list(reversed(colourChoice)) if choice == 'W' else None

    
    if assign_players(choice):
        player1, player2 = assign_players(choice)
        print(f" Player 1 is '{player1}', Player 2 is '{player2}'")
        return assign_players(choice)
    else:
        print(" Invalid choice. Please enter 'B' or 'W'.")
        choose_players_colours()
    

    
def get_user_placement():
    row = int(input("Enter row (1–15): "))
    col = int(input("Enter col (1–15): "))
    if not (1 <= row <= 15 and 1 <= col <= 15):
        print("placement invalid")
        get_user_placement()
    else:
        return row,col

def get_current_stone(players, playerTurn):
    return players[playerTurn]

def handle_turn(grid, players, playerTurn):
    #current_stone = get_current_stone(players, playerTurn)
    
    is_first_turn = (playerTurn == 0)

    # Determine who is playing and which symbol to use
    if is_first_turn and get_current_stone(players, playerTurn) == 'W':
        print("Player 2, Black")
        current_turn = playerTurn + 1

    elif not is_first_turn and get_current_stone(players, playerTurn - 1) == 'W':
        print("Player 1, White")
        current_turn = playerTurn - 1

    elif is_first_turn and get_current_stone(players, playerTurn) == 'B':
        print("Player 1, Black")
        current_turn = playerTurn

    elif not is_first_turn and get_current_stone(players, playerTurn - 1) == 'B':
        print("Player 2, White")
        current_turn = playerTurn

    else:
        return playerTurn  # Safety net; shouldn't hit this

    # Ask for placement and place the stone
    choiceRow, choiceCol = get_user_placement()
    row, col = place_stone(grid, choiceRow, choiceCol, get_current_stone(players, current_turn))

    # Check for win just once
    check_win(grid, row, col, get_current_stone(players, current_turn))

    # Update turn
    return current_turn

def game_engine(grid, players, playerTurn):
    
    print_grid(grid)  # Show the current grid state
    try:
        
        game_engine(grid, players, handle_turn(grid, players, playerTurn))
       
            
        
    except TypeError: 
        print("Cannot place a stone over existing stones, yours or opponents")
        game_engine(grid, players, playerTurn)
    except ValueError:
        print("Invalid input. Use numbers for coordinates.")
        game_engine(grid, players, playerTurn)
    except KeyboardInterrupt:
        print("\nExiting.")  # Exit cleanly on Ctrl+C
        

        

def main():
    playerTurn = 0
    
    players =  list(choose_players_colours())
    grid = create_grid()  # Initialize the grid
    
    
    game_engine(grid, players, playerTurn)

if __name__ == "__main__":
    print(programIntroduction)
    main()  # Start the game