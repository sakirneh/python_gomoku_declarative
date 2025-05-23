# -*- coding: utf-8 -*-
"""
@author: 23178823
"""
import os
import random
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Union

#Stone dataclasses (Black, White, Empty) 
@dataclass(eq=True, frozen=True)
class Black:
    def __str__(self):
        return "B"

@dataclass(eq=True, frozen=True)
class White:
    def __str__(self):
        return "W"

@dataclass(eq=True, frozen=True)
class Empty:
    def __str__(self):
        return "."

Stone = Union[Black, White]
StoneOrEmpty = Union[Black, White, Empty]

#Player dataclass
@dataclass
class Player:
    name: str
    stone: Stone
    is_cpu: bool = False

#Move dataclass
@dataclass
class Move:
    player: Player
    row: int
    col: int

#Board dataclass and logic
@dataclass
class Board:
    size: int = 15
    grid: Tuple[Tuple[StoneOrEmpty, size], size] = field(default_factory=lambda: tuple(tuple(Empty() for _col in range(15)) for _row in range(15))) # type: ignore

    def display(self):
        clear_screen()
        col_numbers = [f"{i+1:>3}" for i in range(self.size)]
        print("   " + "".join(col_numbers))
        self._display_rows_recursive(0)

    def _display_rows_recursive(self, idx: int):
        if idx >= self.size:
            return
        row = self.grid[idx]
        print(f"{idx+1:2} " + "".join(f"{str(cell):>3}" for cell in row))
        self._display_rows_recursive(idx + 1)

    def is_empty(self, r: int, c: int) -> bool:
        return isinstance(self.grid[r][c], Empty)

    def place_stone(self, r: int, c: int, stone: Stone) -> bool:
        if self.is_empty(r, c):
            # Convert the row to a list to allow mutation
            new_row = list(self.grid[r])
            new_row[c] = stone
            # Replace the row in the grid with a new tuple
            new_grid = list(self.grid)
            new_grid[r] = tuple(new_row)
            self.grid = tuple(new_grid) # type: ignore
            return True
        return False

    def is_full(self) -> bool:
        return all(not isinstance(cell, Empty) for row in self.grid for cell in row)

    def check_winner(self, stone: Stone, r: int, c: int) -> bool:
        
        #Recursively check all four directions for five in a row.
        
        
        directions = [(1,0), (0,1), (1,1), (1,-1)]
        return self._check_directions_recursive(stone, r, c, directions, 0)

    def _check_directions_recursive(self, stone: Stone, r: int, c: int, directions: list, idx: int) -> bool:
        
        #Recursively checks each direction for a win.
        
        if idx >= len(directions):
            return False
        dr, dc = directions[idx]
        count = 1 + self._count_direction_recursive(stone, r, c, dr, dc) + self._count_direction_recursive(stone, r, c, -dr, -dc)
        if count >= 5:
            return True
        return self._check_directions_recursive(stone, r, c, directions, idx + 1)

    def _count_direction_recursive(self, stone: Stone, r: int, c: int, dr: int, dc: int) -> int:
        
        #Recursively count consecutive stones in a given direction from (r, c), excluding (r, c) itself.
        
        nr, nc = r + dr, c + dc
        if 0 <= nr < self.size and 0 <= nc < self.size and self.grid[nr][nc] == stone:
            return 1 + self._count_direction_recursive(stone, nr, nc, dr, dc)
        else:
            return 0

#GameState dataclass 
@dataclass
class GameState:
    board: Board
    players: Tuple[Player, Player]
    moves: List[Move] = field(default_factory=list)
    current_player_idx: int = 0
    winner: Optional[Player] = None
    draw: bool = False
    finished: bool = False

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_idx]

    def switch_player(self):
        self.current_player_idx = 1 - self.current_player_idx

    def add_move(self, move: Move):
        self.moves.append(move)

#Utility functions
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    #

def get_valid_name(player_number: int) -> str:
    name = input(f"Enter name for Player {player_number}: ")
    try:
        int(name)
        print("Player name cannot be a number. Please enter a valid name.")
        return get_valid_name(player_number)
    except ValueError:
        pass
    if len(name.strip()) >= 3:
        return name
    print("Player name must be at least 3 characters long.")
    return get_valid_name(player_number)

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

def create_players(mode: str) -> Tuple[Player, Player]:
    name1 = get_valid_name(1)
    if mode == "1":
        colour_choice = choose_player_colour()
        name2 = get_valid_name(2)
        if colour_choice == "1":
            return (Player(name1, Black(), is_cpu=False),Player(name2, White(), is_cpu=False))
        else:
            return (Player(name2, Black(), is_cpu=False), Player(name1, White(), is_cpu=False))
    else:
        colour_choice = choose_player_colour()
        if colour_choice == "1":
            return (Player(name1, Black(), is_cpu=False), Player("CPU", White(), is_cpu=True))
        else:
            return (Player("CPU", Black(), is_cpu=True), Player(name1, White(), is_cpu=False))


def get_user_move(player: Player, board: Board) -> Tuple[int, int]:
    move = input(f"{player.name} ({str(player.stone)}), enter your move (row col): ")
    try:
        r, c = map(int, move.strip().split())
        if 1 <= r <= board.size and 1 <= c <= board.size:
            r0, c0 = r - 1, c - 1
            if board.is_empty(r0, c0):
                return r0, c0
            print("Cell already occupied.")
        else:
            print("Move out of bounds.")
    except ValueError:
        print("Invalid format. Enter row and column as integers.")
    return get_user_move(player, board)

def get_random_empty_coord(board: Board) -> Tuple[int, int]:
    empty_cells = [(r, c) for r in range(board.size) for c in range(board.size) if board.is_empty(r, c)]
    return random.choice(empty_cells)

def cpu_move(game_state: GameState, cpu: Player) -> Tuple[int, int]:
    
    #CPU move logic using recursion.
    #Tries to extend its last move in a random direction, else picks a random empty cell.
    
    moves = [move for move in game_state.moves if move.player.is_cpu]
    if not moves:
        return get_random_empty_coord(game_state.board)
    last_move = moves[-1]
    r0, c0 = last_move.row, last_move.col
    directions = [(1,0), (0,1), (-1,0), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]
    random.shuffle(directions)
    return cpu_move_recursive(game_state.board, r0, c0, directions, 0)

def cpu_move_recursive(board: Board, r0: int, c0: int, directions: list, idx: int) -> Tuple[int, int]:
    if idx >= len(directions):
        return get_random_empty_coord(board)
    dr, dc = directions[idx]
    r1, c1 = r0 + dr, c0 + dc
    if 0 <= r1 < board.size and 0 <= c1 < board.size and board.is_empty(r1, c1):
        return (r1, c1)
    return cpu_move_recursive(board, r0, c0, directions, idx + 1)

#Game engine functions
def play_turn(game_state: GameState):
    player = game_state.current_player
    board = game_state.board
    if player.is_cpu:
        r, c = cpu_move(game_state, player)
    else:
        board.display()
        r, c = get_user_move(player, board)
    board.place_stone(r, c, player.stone)
    game_state.add_move(Move(player, r, c))
    if board.check_winner(player.stone, r, c):
        board.display()
        print(f" {player.name} wins!")
        game_state.winner = player
        game_state.finished = True
        main()
        
    if board.is_full():
        board.display()
        print("It's a draw!")
        game_state.draw = True
        game_state.finished = True
        main()
        
    game_state.switch_player()

def game_loop(game_state: GameState):
    while not game_state.finished:
        play_turn(game_state)
    

# Main entry point
def main():
    
    mode = choose_game_mode()
    player1, player2 = create_players(mode)
    players = (player1, player2)
    if isinstance(players[1].stone, Black):
        players = (players[1], players[0])
    board = Board()
    game_state = GameState(board=board, players=players)
    game_loop(game_state)

if __name__ == "__main__":
    print("Welcome to Gomoku (B = Black, W = White \nBlack always goes first in Gomoku \n")
    main()
