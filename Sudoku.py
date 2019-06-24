# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 08:16:07 2018

@author: J
"""
import numpy as np
from itertools import product
from copy import deepcopy
import time



def format_sudoku(X):
    tmp = '{} {} {}|{} {} {}|{} {} {}\n'
    out = ''
    for i, row in enumerate(X):
        out += tmp.format(*[str(x) for x in row])
        if i in [2, 5]:
            out += '-'*17 + '\n'
    out = out.replace('0', '_')
    return out





def sudokuGenerator(filename):
    # returns a generator that yields sudoku puzzles from a file
    with open(filename) as f:
        header = f.readline()

        while header != '':
            string = ''
            for i in range(9):
                string += f.readline()

            yield fromString(string)
            header = f.readline()



def fromString(string, empty='0'):
    values = []
    string = string.replace(empty, '0')
    for line in string.split():
        values.append([int(x) for x in line])
    return np.array(values)




def solve(X, moves = []):
    # Recusrive function that solves sudoku puzzles. deduces the next best move
    # and enters the function again. Returns the complete puzzle, or None if no
    # solution can be found.
    X = deepcopy(X)
    # [list/set of possible entries, y position, x position, if it was guessed]
    best_guess = [[None]*100, 0, 0, False]
    for i, j in product(range(9), range(9)):
        if X[i, j] != 0:
            continue
        possibilities = set(range(1, 10))
        possibilities -= set(X[i, :]) # eliminate values in same row
        possibilities -= set(X[:, j]) # eliminate values in same column
        # Eliminate values in same 3x3 square
        possibilities -= set(X[i//3*3:(i//3 + 1)*3, j//3*3:(j//3 + 1)*3].ravel())

        if len(possibilities) == 0:
            # if there are no possible entries in an empty square,
            # the puzzle is invalid.
            return None, None
        elif len(possibilities) < len(best_guess[0]):
            # keep the value and position of the square with the least possible
            # entries
            best_guess = [possibilities, i, j]

    if None in best_guess[0]:
        # The puzzle is solved if no more guesses are made.
        return X, moves
    for entry in best_guess[0]:
        # make one move and recurse.
        X[best_guess[1], best_guess[2]] = entry
        guessed = len(best_guess[0]) > 1
        XX, theseMoves = solve(X, moves=moves + [[entry, best_guess[1], best_guess[2], guessed]])
        if XX is not None:
            # If a valid solution is returned, close the recursive loop
            return XX, theseMoves
    # if none of the guesses yielded a solution, yield nothing.
    return None, None





if __name__ == '__main__':
    filename = 'data/p096_sudoku.txt'
    now = time.time()
    for i, X in enumerate(sudokuGenerator(filename)):
        XX, moves = solve(X)
        print(format_sudoku(XX))

    print('Time: ', time.time()-now)
