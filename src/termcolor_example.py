import Sudoku
import time
import os
import numpy as np

filename = 'data/sudoku_puzzle.txt'


with open(filename) as f:
    X = Sudoku.fromString(f.read(), empty='_')

_, moves = Sudoku.solve(X)
mask = np.zeros([9, 9])
Sudoku.print_sudoku(X, mask)

for val, x, y, guessed in moves:
    X[x, y] = val
    mask[x, y] = 1
    os.system('clear')
    Sudoku.print_sudoku(X, mask)
    if guessed:
        print('GUESS!')
    print()
    time.sleep(0.5)
