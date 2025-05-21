# -*- coding: utf-8 -*-
"""
@author: 23178823
"""
import os
import random
from dataclasses import dataclass
from typing import TypeAlias, Union

# --- Constants ---
GRID_SIZE = 15                   # The size of the Gomoku board (15x15 standard)
EMPTY_CELL = "."                 # Symbol to represent an empty cell on the board

# --- Utility Functions ---
def clear_screen():
    # Clear the terminal screen before displaying the board
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    

# --- Stone Types ---
@dataclass(eq=True, frozen=True)
class Black:
    # Represents a black stone
    def __str__(self):
        return "B"

@dataclass(eq=True, frozen=True)
class White:
    # Represents a white stone
    def __str__(self):
        return "W"

# Define the type alias for a stone, which can be Black or White
Stone: TypeAlias = Union[Black, White]

# --- Player Base ---
class Player:
    # Represents a human player
    def __init__(self, name: str, stone: Stone):
        self.name = name
        self.stone = stone

    def __str__(self):
        # String representation showing player name and stone color
        return f"{self.name} ({self.stone})"

    def get_move(self, grid) -> tuple[int, int]:
        # Ask the user for their move
        return get_user_move(self, grid)

# --- CPU Opponent ---
class CpuPlayer(Player):
    # Represents a CPU player with simple "chaining" logic
    def __init__(self, name: str, stone: Stone):
        super().__init__(name, stone)
        self.last_move = None  # Track the last CPU move (row, col)

    def get_move(self, grid) -> tuple[int, int]:
        # If no previous move, pick a random empty cell
        if self.last_move is None:
            move = get_random_empty_coord(grid)
            self.last_move = move
            return move

        # Try to extend from the last move in a random direction
        r0, c0 = self.last_move
        # All 8 possible directions (right, down, left, up, and diagonals)
        directions = [(1,0), (0,1), (-1,0), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]
        random.shuffle(directions)  # Randomize direction choice
        for dr, dc in directions:
            r1, c1 = r0 + dr, c0 + dc
            # If the adjacent cell is within bounds and empty, go there
            if 0 <= r1 < grid.size and 0 <= c1 < grid.size and grid.is_empty(r1, c1):
                self.last_move = (r1, c1)
                return (r1, c1)

        # If blocked on all sides, pick a new random empty cell and start a new chain
        move = get_random_empty_coord(grid)
        self.last_move = move
        return move

# --- Grid Class ---
class Grid:
    # The immutable board class made of tuples
    def __init__(self, size: int = GRID_SIZE, board: tuple = None):
        self.size = size
        if board is None:
            # Create an empty board (tuple of tuples)
            self.board = tuple(tuple(EMPTY_CELL for _cell in range(size)) for _row in range(size))
        else:
            # Use the provided board (used for immutability)
            self.board = board

    def display(self) -> None:
        # Clear the screen before displaying the board
        clear_screen()
        # Print the column numbers as header (aligned)
        col_numbers = [f"{i+1:>3}" for i in range(self.size)]
        print("   " + "".join(col_numbers))
        # Print each row with its number and the cell contents
        for idx, row in enumerate(self.board):
            print(f"{idx+1:2} " + "".join(f"{cell:>3}" for cell in row))

    def is_empty(self, r: int, c: int) -> bool:
        # Check if a given cell is empty
        return self.board[r][c] == EMPTY_CELL

    def place_stone(self, r: int, c: int, stone: Stone) -> 'Grid':
        # Place a stone at (r, c) by creating a new grid (immutability)
        new_row = self.board[r][:c] + (str(stone),) + self.board[r][c+1:]
        new_board = self.board[:r] + (new_row,) + self.board[r+1:]
        return Grid(self.size, new_board)

    def is_full(self) -> bool:
        # Return True if there are no empty cells left
        return all(cell != EMPTY_CELL for row in self.board for cell in row)

    def check_winner(self, stone: Stone, r: int, c: int) -> bool:
        # Check if placing stone at (r, c) creates a five-in-a-row for that stone
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # Horizontal, vertical, 2 diagonals
        return any(self.count_consecutive(stone, r, c, dx, dy) >= 5 for dx, dy in directions)

    def count_consecutive(self, stone: Stone, r: int, c: int, dx: int, dy: int) -> int:
        # Count consecutive stones of the same color from (r, c) in both directions
        return 1 + self.count_direction(stone, r, c, dx, dy, 1) + self.count_direction(stone, r, c, dx, dy, -1)

    def count_direction(self, stone: Stone, r: int, c: int, dx: int, dy: int, direction: int, i: int = 1) -> int:
        # Count consecutive stones in a single direction (used by count_consecutive)
        nr, nc = r + direction * i * dx, c + direction * i * dy
        if 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr][nc] == str(stone):
            return 1 + self.count_direction(stone, r, c, dx, dy, direction, i + 1)
        else:
            return 0

# --- Input / Game Setup ---

def choose_game_mode() -> str:
    # Ask user for game mode (PvP or PvCPU)
    print("Select Game Mode:")
    print("1. Player vs Player")
    print("2. Player vs CPU")
    return choose_game_mode_helper()

def choose_game_mode_helper() -> str:
    # Helper for input validation for game mode
    choice = input("Enter choice (1 or 2): ").strip()
    if choice in ("1", "2"):
        return choice
    print("Invalid input. Please enter 1 or 2.")
    return choose_game_mode_helper()

def choose_player_colour() -> str:
    # Ask user for their chosen color (Black or White)
    print("Choose your colour:")
    print("1. Black (B, goes first)")
    print("2. White (W, goes second)")
    return choose_player_colour_helper()

def choose_player_colour_helper() -> str:
    # Helper for input validation for player color
    choice = input("Enter choice (1 for Black, 2 for White): ").strip()
    if choice in ("1", "2"):
        return choice
    print("Invalid input. Please enter 1 or 2.")
    return choose_player_colour_helper()

def create_players(mode: str) -> tuple[Player, Player]:
    # Recursive helper to get a valid player name
    def get_valid_name(player_number: int) -> str:
        name = input(f"Enter name for Player {player_number}: ")
        if len(name.strip()) >= 3:
            return name
        print("Player name must be at least 3 characters long.")
        return get_valid_name(player_number)

    name1 = get_valid_name(1)
    if mode == "1":
        name2 = get_valid_name(2)
        return Player(name1, Black()), Player(name2, White())
    else:
        colour_choice = choose_player_colour()
        if colour_choice == "1":
            # Player chooses Black, CPU is White
            return Player(name1, Black()), CpuPlayer("CPU", White())
        else:
            # Player chooses White, CPU is Black
            return CpuPlayer("CPU", Black()), Player(name1, White())

def get_user_move(player: Player, grid: Grid) -> tuple[int, int]:
    # Get a move from a human player (with input validation)
    return get_user_move_helper(player, grid)

def get_user_move_helper(player: Player, grid: Grid) -> tuple[int, int]:
    # Helper function: repeatedly ask until a valid move is entered
    move = input(f"{player}, enter your move (row col): ")
    try:
        r, c = map(int, move.strip().split())
        if 1 <= r <= grid.size and 1 <= c <= grid.size:
            # Adjust for 0-based index
            r0, c0 = r - 1, c - 1
            if grid.is_empty(r0, c0):
                return r0, c0
            print("Cell already occupied.")
        else:
            print("Move out of bounds.")
    except ValueError:
        print("Invalid format. Enter row and column as integers.")
    return get_user_move_helper(player, grid)

def get_random_empty_coord(grid: Grid) -> tuple[int, int]:
    # Get a random empty cell from the grid
    empty_cells = [(r, c) for r in range(grid.size) for c in range(grid.size) if grid.is_empty(r, c)]
    return random.choice(empty_cells)

# --- Game Engine ---

def play_turn(player: Player, grid: Grid) -> tuple[Grid, int, int]:
    # Play a single turn: get move, place stone, return updated grid and move location
    r, c = player.get_move(grid)
    updated_grid = grid.place_stone(r, c, player.stone)
    return updated_grid, r, c

def game_loop(player1: Player, player2: Player) -> None:
    # Main game loop: set up initial grid and start turn sequence
    grid = Grid()
    current_player = player1
    
    game_loop_step(grid, current_player, player1, player2)

def game_loop_step(grid: Grid, current_player: Player, player1: Player, player2: Player) -> None:
    # Only display the board if it's a human player
    if not isinstance(current_player, CpuPlayer):
        grid.display()
    
        

    grid, r, c = play_turn(current_player, grid)

    # After a move, check for win/draw
    if grid.check_winner(current_player.stone, r, c):
        grid.display()  # Always show the final board
        print(f" {current_player.name} wins!")
        return

    if grid.is_full():
        grid.display()  # Always show the final board
        print("It's a draw!")
        return

    next_player = player2 if current_player == player1 else player1
    game_loop_step(grid, next_player, player1, player2)

# --- Main Entry Point ---

def main():
    # Entry point: setup and start the game
    
    mode = choose_game_mode()
    player1, player2 = create_players(mode)
    game_loop(player1, player2)

if __name__ == "__main__":
    
    print("Welcome to Gomoku (B = Black, W = White)")
    print("Black always goes first in Gomoku \n")

    main()