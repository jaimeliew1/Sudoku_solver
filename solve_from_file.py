import Sudoku
import time
import os
import matplotlib.pyplot as plt
import numpy as np

filename = 'sudoku_puzzle.txt'
with open(filename) as f:
    X = Sudoku.fromString(f.read(), empty='_')

XX, moves = Sudoku.solve(X)

    #time.sleep(0.1)
    #os.system('cls')

print(Sudoku.format_sudoku(X))
plt.figure(figsize=[10,10])
for move in moves:
    plt.cla()
    print(Sudoku.format_sudoku(X))
    val, x, y, guessed = move
    X[x, y] = val
    X_strings = [str(x) if x>0 else '' for x in X.ravel()]
    X_strings = np.reshape(X_strings, [9, 9])
    table = plt.table(cellText=X_strings, loc='center', cellLoc='center')
    table.set_fontsize(30)
    table.scale(1, 4)
    plt.axis('tight')
    plt.axis('off')
    plt.axis('equal')
    plt.draw()
    plt.pause(0.1)
plt.show()
