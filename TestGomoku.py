# -*- coding: utf-8 -*-
"""
Created on Sun May 18 12:57:39 2025

@author: henrikas
"""

import unittest
from unittest.mock import patch
from gomoku2 import Grid, Black, White, Player, CpuPlayer, EMPTY_CELL, Stone, GRID_SIZE

class TestGomokuCore(unittest.TestCase):
    def setUp(self):
        self.grid = Grid(5)

    def test_grid_initialization(self):
        grid = Grid(4)
        self.assertEqual(len(grid.board), 4)
        for row in grid.board:
            self.assertEqual(len(row), 4)
            for cell in row:
                self.assertEqual(cell, EMPTY_CELL)

    def test_is_empty_and_place_stone(self):
        self.assertTrue(self.grid.is_empty(0, 0))
        new_grid = self.grid.place_stone(0, 0, Black())
        self.assertFalse(new_grid.is_empty(0, 0))
        self.assertEqual(new_grid.board[0][0], "B")
        # Immutability test
        self.assertTrue(self.grid.is_empty(0, 0))

    def test_is_full(self):
        size = 3
        grid = Grid(size)
        for r in range(size):
            for c in range(size):
                grid = grid.place_stone(r, c, Black())
        self.assertTrue(grid.is_full())
        # Not full
        grid2 = Grid(size)
        grid2 = grid2.place_stone(0, 0, White())
        self.assertFalse(grid2.is_full())

    def test_check_winner_horizontal(self):
        grid = Grid(5)
        for c in range(5):
            grid = grid.place_stone(2, c, Black())
        self.assertTrue(grid.check_winner(Black(), 2, 2))

    def test_check_winner_vertical(self):
        grid = Grid(5)
        for r in range(5):
            grid = grid.place_stone(r, 3, White())
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
        grid = grid.place_stone(1, 1, Black())
        grid = grid.place_stone(2, 2, Black())
        grid = grid.place_stone(3, 3, Black())
        # Diagonal (1,1)-(2,2)-(3,3)
        self.assertEqual(grid.count_consecutive(Black(), 2, 2, 1, 1), 3)
        # Horizontal only 1 at (2,2)
        self.assertEqual(grid.count_consecutive(Black(), 2, 2, 0, 1), 1)

    def test_player_and_cpuplayer_str(self):
        p = Player("Alice", Black())
        cpu = CpuPlayer("CPU", White())
        self.assertEqual(str(p), "Alice (B)")
        self.assertEqual(str(cpu), "CPU (W)")

    def test_cpu_player_selects_valid_move(self):
        grid = Grid(3)
        # Fill all but one cell
        for r in range(3):
            for c in range(3):
                if (r, c) != (1, 1):
                    grid = grid.place_stone(r, c, Black())
        cpu = CpuPlayer("CPU", White())
        move = cpu.get_move(grid)
        self.assertEqual(move, (1, 1))

    def test_grid_display_does_not_crash(self):
        # Just ensure display works (visually inspected)
        grid = Grid(3)
        try:
            grid.display()
        except Exception as e:
            self.fail(f"display() raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()