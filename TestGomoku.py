# -*- coding: utf-8 -*-
"""
@author: 23178823
"""

import unittest
from Gomoku import Black, White, Empty, Player, Move, Board, GameState, cpu_move

class TestGomoku(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.player_black = Player("BlackPlayer", Black())
        self.player_white = Player("WhitePlayer", White())

    def test_board_initialization(self):
        self.assertEqual(len(self.board.grid), 15)
        for row in self.board.grid:
            self.assertEqual(len(row), 15)
            for cell in row:
                self.assertIsInstance(cell, Empty)

    def test_place_and_is_empty(self):
        r, c = 7, 7
        self.assertTrue(self.board.is_empty(r, c))
        placed = self.board.place_stone(r, c, Black())
        self.assertTrue(placed)
        self.assertFalse(self.board.is_empty(r, c))
        # Try to place again
        placed_again = self.board.place_stone(r, c, White())
        self.assertFalse(placed_again)

    def test_is_full(self):
        # Fill the board with alternating stones
        for r in range(self.board.size):
            for c in range(self.board.size):
                self.board.place_stone(r, c, Black() if (r + c) % 2 == 0 else White())
        self.assertTrue(self.board.is_full())

    def test_check_winner_horizontal(self):
        r = 5
        for c in range(5):
            self.board.place_stone(r, c, Black())
        self.assertTrue(self.board.check_winner(Black(), r, 2))
        self.assertFalse(self.board.check_winner(White(), r, 2))

    def test_check_winner_vertical(self):
        c = 3
        for r in range(5):
            self.board.place_stone(r, c, White())
        self.assertTrue(self.board.check_winner(White(), 2, c))
        self.assertFalse(self.board.check_winner(Black(), 2, c))

    def test_check_winner_diagonal(self):
        for i in range(5):
            self.board.place_stone(i, i, Black())
        self.assertTrue(self.board.check_winner(Black(), 2, 2))

    def test_check_winner_antidiagonal(self):
        for i in range(5):
            self.board.place_stone(i, 4 - i, White())
        self.assertTrue(self.board.check_winner(White(), 2, 2))

    def test_game_state_switch_and_current(self):
        gs = GameState(self.board, (self.player_black, self.player_white))
        self.assertEqual(gs.current_player, self.player_black)
        gs.switch_player()
        self.assertEqual(gs.current_player, self.player_white)
        gs.switch_player()
        self.assertEqual(gs.current_player, self.player_black)

    def test_move_history(self):
        gs = GameState(self.board, (self.player_black, self.player_white))
        move = Move(self.player_black, 0, 0)
        gs.add_move(move)
        self.assertEqual(len(gs.moves), 1)
        self.assertEqual(gs.moves[0], move)


    def test_cpu_move(self):
        
        gs = GameState(self.board, (self.player_black, Player("CPU", White(), is_cpu=True)))
        move = cpu_move(gs, gs.players[1])
        self.assertIsInstance(move, tuple)
        self.assertEqual(len(move), 2)
        r, c = move
        self.assertTrue(self.board.is_empty(r, c))

if __name__ == "__main__":
    unittest.main()