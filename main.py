import os
from time import sleep
from colorama import Fore,Back,Style
import numpy as np
#int: boardGameSize = 8
#int: winInARow = 5
#bool: keepLooping = true


"""
+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
|    |    |    |    |    |    |    |    |    |    |    |    |    |    |
+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
|    |    |    |    |    |    |    |    |    |    |    |    |    |    |
+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
|    |    |    |    |    |    |    |    |    |    |    |    |    |    |
+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
|    |    |    |    |    |    |    |    |    |    |    |    |    |    |
+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
|    |    |    |    |    |    |    |    |    |    |    |    |    |    |
+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
|    |    |    |    |    |    |    |    |    |    |    |    |    |    |
+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
|    |    |    |    |    |    |    |    |    |    |    |    |    |    |
+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
|    |    |    |    |    |    |    |    |    |    |    |    |    |    |
+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
|    |    |    |    |    |    |    |    |    |    |    |    |    |    |
+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
|    |    |    |    |    |    |    |    |    |    |    |    |    |    |
+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
|    |    |    |    |    |    |    |    |    |    |    |    |    |    |
+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
|    |    |    |    |    |    |    |    |    |    |    |    |    |    |
+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
|    |    |    |    |    |    |    |    |    |    |    |    |    |    |
+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
|    |    |    |    |    |    |    |    |    |    |    |    |    |    |
+----+----+----+----+----+----+----+----+----+----+----+----+----+----+



"""

#print("Gomoku game by Henrikas Varanauskas - board size 15x15")
def placeStone():
    pass
def validPlacement():
    pass


def createBoard():
    board = np.zeros((16,16))
    return board


def gameLoop(playerTurn: int):

    finished: bool = False
    while not finished:
        
        board = createBoard()
        # create board
        #print(board)
        """
        for row in range(len(board)):
            for column in range(len(board)):
                print(board[row][column], end="xd ")
        
        """
        """
        print("+----+----+----+----+----+----+----+----+----+----+----+----+----+----+")
        for row in range(len(board)):
            
            for column in range(len(board)):
                
                print(board[row][column], end="|")
    
        """
        #newBoard = [[board[row][column] for row in range(len(board))] for column in range(len(board)) ]
        
        
        #player 1 selection
        if playerTurn == 1:
            selection: str = input("Player 1 select at which intersection to place stone. e.g. a3: ")
        
        else:
            selection: str = input("Player 2 select at which intersection to place stone. e.g. a3: ")
        
        playerTurn +=1
        playerTurn = playerTurn %2
        sleep(1)


#initial statements



def create_grid(rows=14, cols=14):
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

    # Column headers (1 to 16)
    print("   ", end="")  # space for row labels
    for col in range(1, num_cols + 1):
        print(f"{col:>2}", end="  ")
    print()

    for r_idx, row in enumerate(grid):
        if r_idx % 2 == 0:
            row_label = f"{r_idx // 2 + 1:>2}  "
        else:
            row_label = "    "
        print(row_label + "".join(row))

def change_plus(grid, row, col):
    # Adjust for 1-based input
    stone:chr = 'O'
    r = (row - 1) * 2
    c = (col - 1) * 2
    if 0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c] == '+':
        grid[r][c] = 'O'
        print(f"Changed '+' at ({row}, {col}) to '{stone}'")
    else:
        print("Not a valid placement")
        

def main():
    grid = create_grid()
    while True:
        os.system('cls')
        
        print_grid(grid)
        try:
            row = int(input("Enter row (1–15): "))
            col = int(input("Enter col (1–15): "))
            if not (1 <= row <= 15 and 1 <= col <= 15):
                print(" Out of range. Try again.")
                continue
            """
            new_char = input("Enter new character to replace '+': ")
            if len(new_char) != 1:
                print(" Enter a single character only.")
                continue
            """
            change_plus(grid, row, col)
        except ValueError:
            print("Invalid input. Use numbers for coordinates.")
        except KeyboardInterrupt:
            print("\n Exiting.")
            break

if __name__ == "__main__":
    main()
