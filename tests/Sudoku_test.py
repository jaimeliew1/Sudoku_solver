# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 08:19:32 2018

@author: J
"""

import unittest
import Sudoku
import numpy as np

class TestSudoku(unittest.TestCase):

    def test_puzzle1(self):
        unsolved = Sudoku.fromString('''003020600
900305001
001806400
008102900
700000008
006708200
002609500
800203009
005010300''')
        solved = np.array([[4, 8, 3, 9, 2, 1, 6, 5, 7],
       [9, 6, 7, 3, 4, 5, 8, 2, 1],
       [2, 5, 1, 8, 7, 6, 4, 9, 3],
       [5, 4, 8, 1, 3, 2, 9, 7, 6],
       [7, 2, 9, 5, 6, 4, 1, 3, 8],
       [1, 3, 6, 7, 9, 8, 2, 4, 5],
       [3, 7, 2, 6, 8, 9, 5, 1, 4],
       [8, 1, 4, 2, 5, 3, 7, 6, 9],
       [6, 9, 5, 4, 1, 7, 3, 8, 2]])

        self.assertTrue((solved ==Sudoku.solve(unsolved).values).all())

    def test_puzzle2(self):
        unsolved = Sudoku.fromString('''200080300
060070084
030500209
000105408
000000000
402706000
301007040
720040060
004010003''')
        solved = np.array([[2, 4, 5, 9, 8, 1, 3, 7, 6],
       [1, 6, 9, 2, 7, 3, 5, 8, 4],
       [8, 3, 7, 5, 6, 4, 2, 1, 9],
       [9, 7, 6, 1, 2, 5, 4, 3, 8],
       [5, 1, 3, 4, 9, 8, 6, 2, 7],
       [4, 8, 2, 7, 3, 6, 9, 5, 1],
       [3, 9, 1, 6, 5, 7, 8, 4, 2],
       [7, 2, 8, 3, 4, 9, 1, 6, 5],
       [6, 5, 4, 8, 1, 2, 7, 9, 3]])

        self.assertTrue((solved == Sudoku.solve(unsolved).values).all())

if __name__ == '__main__':
    unittest.main()