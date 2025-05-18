# -*- coding: utf-8 -*-
"""
Created on Sun May 18 12:57:39 2025

@author: henrikas
"""

import unittest
from gomoku2 import Grid, Black, White, Player, CpuPlayer, EMPTY_CELL

class TestGomoku(unittest.TestCase):
    def setUp(self):
        self.grid = Grid(5)

    def test_is_empty_and_place_stone(self):
        # All cells should be empty at start
        for r in range(self.grid.size):
            for c in range(self.grid.size):
                self.assertTrue(self.grid.is_empty(r, c))
        # Place a black stone
        grid2 = self.grid.place_stone(2, 2, Black())
        self.assertFalse(grid2.is_empty(2, 2))
        self.assertEqual(grid2.board[2][2], "B")
        # Original grid is unchanged (immutability)
        self.assertTrue(self.grid.is_empty(2, 2))

    def test_is_full(self):
        # Empty grid is not full
        self.assertFalse(self.grid.is_full())
        # Fill grid
        filled = Grid(2)
        for r in range(2):
            for c in range(2):
                filled = filled.place_stone(r, c, Black() if (r+c)%2==0 else White())
        self.assertTrue(filled.is_full())

    def test_check_winner_horizontal(self):
        grid = Grid(5)
        for i in range(5):
            grid = grid.place_stone(2, i, Black())
        self.assertTrue(grid.check_winner(Black(), 2, 2))

    def test_check_winner_vertical(self):
        grid = Grid(5)
        for i in range(5):
            grid = grid.place_stone(i, 3, White())
        self.assertTrue(grid.check_winner(White(), 2, 3))

    def test_check_winner_diagonal(self):
        grid = Grid(5)
        for i in range(5):
            grid = grid.place_stone(i, i, Black())
        self.assertTrue(grid.check_winner(Black(), 2, 2))

    def test_check_winner_anti_diagonal(self):
        grid = Grid(5)
        for i in range(5):
            grid = grid.place_stone(i, 4-i, White())
        self.assertTrue(grid.check_winner(White(), 2, 2))

    def test_count_consecutive_and_direction(self):
        grid = Grid(5)
        # Place some stones: 1,1 B; 2,2 B; 3,3 B
        grid = grid.place_stone(1, 1, Black())
        grid = grid.place_stone(2, 2, Black())
        grid = grid.place_stone(3, 3, Black())
        # Should count 3 in diagonal direction from (2,2)
        self.assertEqual(grid.count_consecutive(Black(), 2, 2, 1, 1), 3)
        # Should count 1 in horizontal direction from (2,2)
        self.assertEqual(grid.count_consecutive(Black(), 2, 2, 0, 1), 1)

    def test_cpu_player_moves_on_empty_cell(self):
        grid = Grid(3)
        cpu = CpuPlayer("CPU", Black())
        # fill all but one cell
        for r in range(3):
            for c in range(3):
                if not (r == 1 and c == 1):
                    grid = grid.place_stone(r, c, Black())
        move = cpu.get_move(grid)
        self.assertEqual(move, (1, 1))

    def test_player_str(self):
        player = Player("Alice", Black())
        self.assertEqual(str(player), "Alice (B)")

    def test_grid_display_runs(self):
        # Just verify that display does not crash (visual check/manual)
        grid = Grid(3)
        grid.display()

if __name__ == '__main__':
    unittest.main()