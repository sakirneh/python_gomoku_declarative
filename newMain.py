# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import TypeAlias

programIntroduction : str = """
Gomoku game
By Henrikas Varanauskas
ID 23178823
2025

"""

# X
@dataclass(eq=True, frozen=True)
class B:
    def __str__(self):
         return "B"
    # O
@dataclass(eq=True, frozen=True)
class W:
    def __str__(self):
         return "W"
# Let Token = {B} U {W}
# Let Token = {B, W}
Stone: TypeAlias = B | W


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

def update_grid(grid, r, c, new_char):
    """Replace the '+' at position (r, c) with the new character."""
    return grid[r][:c] + [new_char] + grid[r][c + 1:]

def place_stone(grid, row, col, stone):
    
    r, c = get_grid_index(row, col)
    if is_valid_position(grid, r, c):
        grid[r] = update_grid(grid, r, c, stone)
        
        return r, c
    
        

        
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
    
    # Determine who's playing and print appropriate label
    if is_first_turn and get_current_stone(players, playerTurn) == 'W':
        print("Player 2, Black")  # Black starts first, player chose White
        choiceRow, choiceCol = get_user_placement()
        playerTurn += 1
        row, col = place_stone(grid, choiceRow, choiceCol, get_current_stone(players, playerTurn))
    
    elif not is_first_turn and get_current_stone(players, playerTurn - 1) == 'W':
        print("Player 1, White")
        choiceRow, choiceCol = get_user_placement()
        playerTurn -= 1
        row, col = place_stone(grid, choiceRow, choiceCol, get_current_stone(players, playerTurn))
    
    elif is_first_turn and get_current_stone(players, playerTurn) == 'B':
        print("Player 1, Black")  # Player chose Black and goes first
        choiceRow, choiceCol = get_user_placement()
        row, col = place_stone(grid, choiceRow, choiceCol, get_current_stone(players, playerTurn))
        playerTurn += 1
    
    elif not is_first_turn and get_current_stone(players, playerTurn - 1) == 'B':
        print("Player 2, White")
        choiceRow, choiceCol = get_user_placement()
        row, col = place_stone(grid, choiceRow, choiceCol, get_current_stone(players, playerTurn))
        playerTurn -= 1

    return playerTurn

def game_engine(grid, players, playerTurn):
    
    print_grid(grid)  # Show the current grid state
    try:
        # Get row and column input from user
        
        #playerStone = get_player_stone(players, playerTurn)
        #print(type(playerStone))
        """
        if(playerTurn == 0 and get_current_stone(players, playerTurn) == 'W'):
            #player chose white but black starts first
            print("Player 2, Black")
            choiceRow,choiceCol = get_user_placement()
            playerTurn +=1
            row, col = place_stone(grid, choiceRow,choiceCol, get_current_stone(players, playerTurn ))
            
            game_engine(grid, players, playerTurn)
            
        
        if(playerTurn == 1 and get_current_stone(players, playerTurn-1) == 'W'):
            print("Player 1, White")
            choiceRow,choiceCol = get_user_placement()
            playerTurn -=1
            row, col = place_stone(grid, choiceRow,choiceCol, get_current_stone(players, playerTurn ))
            
            game_engine(grid, players, playerTurn)
            
        if(playerTurn == 0 and get_current_stone(players, playerTurn) == 'B'):
            #player chose black and black starts first
            print("Player 1, Black")
            choiceRow,choiceCol = get_user_placement()
            row, col = place_stone(grid, choiceRow,choiceCol, get_current_stone(players, playerTurn ))
            
            playerTurn +=1
            game_engine(grid, players, playerTurn)
            
        
            
            
        if(playerTurn == 1 and get_current_stone(players, playerTurn-1) == 'B'):
            print("Player 2, White")
            choiceRow,choiceCol = get_user_placement()
            row, col = place_stone(grid, choiceRow,choiceCol, get_current_stone(players, playerTurn ))
           
            playerTurn -=1
            game_engine(grid, players, playerTurn)
            
       """
       
        game_engine(grid, players, handle_turn(grid, players, playerTurn))
       
            
        
    except TypeError:
        print("cannot unpack non iterable non type")
        game_engine(grid, players, playerTurn)
    except ValueError:
        print("Invalid input. Use numbers for coordinates.")
        game_engine(grid, players, playerTurn)
    except KeyboardInterrupt:
        print("\nExiting.")  # Exit cleanly on Ctrl+C
        

        

def main():
    playerTurn = 0
    #valid_choices = {'B', 'W'}
    
    players =  list(choose_players_colours())
    grid = create_grid()  # Initialize the grid
    
    #print(players.__getitem__(playerTurn))
    
    game_engine(grid, players, playerTurn)

if __name__ == "__main__":
    print(programIntroduction)
    main()  # Start the game