# -*- coding: utf-8 -*-
"""
Created on Sun May 18 12:33:25 2025

@author: henrikas
"""

import sys
import random
from dataclasses import dataclass
from typing import TypeAlias, Union, Optional

# --- Constants ---
GRID_SIZE = 15
EMPTY_CELL = "."

# --- Stone Types ---
@dataclass(eq=True, frozen=True)
class Black:
    def __str__(self): return "B"

@dataclass(eq=True, frozen=True)
class White:
    def __str__(self): return "W"

Stone: TypeAlias = Union[Black, White]

# --- Player Base ---
class Player:
    def __init__(self, name: str, stone: Stone):
        self.name = name
        self.stone = stone

    def __str__(self):
        return f"{self.name} ({self.stone})"

    def get_move(self, grid) -> tuple[int, int]:
        return get_user_move(self, grid)

# --- CPU Opponent ---
class CpuPlayer(Player):
    def get_move(self, grid) -> tuple[int, int]:
        return get_random_empty_coord(grid)

# --- Grid Class ---
class Grid:
    def __init__(self, size: int = GRID_SIZE):
        self.size = size
        self.board = [[EMPTY_CELL for _ in range(size)] for _ in range(size)]

    def display(self) -> None:
        # Use 3 spaces per column: header and cell content are both 3 chars wide, right-aligned
        col_numbers = [f"{i+1:>3}" for i in range(self.size)]
        print("   " + "".join(col_numbers))
        for idx, row in enumerate(self.board):
            print(f"{idx+1:2} " + "".join(f"{cell:>3}" for cell in row))

    def is_empty(self, r: int, c: int) -> bool:
        return self.board[r][c] == EMPTY_CELL

    def place_stone(self, r: int, c: int, stone: Stone) -> 'Grid':
        new_grid = Grid(self.size)
        new_grid.board = [row[:] for row in self.board]
        new_grid.board[r][c] = str(stone)
        return new_grid

    def is_full(self) -> bool:
        return all(cell != EMPTY_CELL for row in self.board for cell in row)

    def check_winner(self, stone: Stone, r: int, c: int) -> bool:
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        return any(self.count_consecutive(stone, r, c, dx, dy) >= 5 for dx, dy in directions)

    def count_consecutive(self, stone: Stone, r: int, c: int, dx: int, dy: int) -> int:
        # Returns total consecutive stones in both directions including the origin cell.
        return 1 + self.count_direction(stone, r, c, dx, dy, 1) + self.count_direction(stone, r, c, dx, dy, -1)

    def count_direction(self, stone: Stone, r: int, c: int, dx: int, dy: int, direction: int, i: int = 1) -> int:
        nr, nc = r + direction * i * dx, c + direction * i * dy
        if 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr][nc] == str(stone):
            return 1 + self.count_direction(stone, r, c, dx, dy, direction, i + 1)
        else:
            return 0

# --- Input / Game Setup ---

def choose_game_mode() -> str:
    print("Select Game Mode:")
    print("1. Player vs Player")
    print("2. Player vs CPU")
    return choose_game_mode_helper()

def choose_game_mode_helper() -> str:
    choice = input("Enter choice (1 or 2): ").strip()
    if choice in ("1", "2"):
        return choice
    print("Invalid input. Please enter 1 or 2.")
    return choose_game_mode_helper()

def choose_player_colour() -> str:
    print("Choose your colour:")
    print("1. Black (B, goes first)")
    print("2. White (W, goes second)")
    return choose_player_colour_helper()

def choose_player_colour_helper() -> str:
    choice = input("Enter choice (1 for Black, 2 for White): ").strip()
    if choice in ("1", "2"):
        return choice
    print("Invalid input. Please enter 1 or 2.")
    return choose_player_colour_helper()

def create_players(mode: str) -> tuple[Player, Player]:
    name1 = input("Enter name for Player 1: ")
    if mode == "1":
        name2 = input("Enter name for Player 2: ")
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
    return get_user_move_helper(player, grid)

def get_user_move_helper(player: Player, grid: Grid) -> tuple[int, int]:
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
    empty_cells = [(r, c) for r in range(grid.size) for c in range(grid.size) if grid.is_empty(r, c)]
    return random.choice(empty_cells)

# --- Game Engine ---

def play_turn(player: Player, grid: Grid) -> tuple[Grid, int, int]:
    r, c = player.get_move(grid)
    updated_grid = grid.place_stone(r, c, player.stone)
    return updated_grid, r, c

def game_loop(player1: Player, player2: Player) -> None:
    grid = Grid()
    current_player = player1
    grid.display()
    game_loop_step(grid, current_player, player1, player2)

def game_loop_step(grid: Grid, current_player: Player, player1: Player, player2: Player) -> None:
    grid, r, c = play_turn(current_player, grid)
    grid.display()

    if grid.check_winner(current_player.stone, r, c):
        print(f"🎉 {current_player.name} wins!")
        return

    if grid.is_full():
        print("It's a draw!")
        return

    next_player = player2 if current_player == player1 else player1
    game_loop_step(grid, next_player, player1, player2)

# --- Main Entry Point ---

def main():
    print("Welcome to Gomoku (B = Black, W = White)")
    mode = choose_game_mode()
    player1, player2 = create_players(mode)
    game_loop(player1, player2)

if __name__ == "__main__":
    main()