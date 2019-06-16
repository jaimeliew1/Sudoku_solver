# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 08:16:07 2018

@author: J
"""
import numpy as np
from itertools import product
from copy import deepcopy
import time



def format_grid(X):
    tmp = '{} {} {}|{} {} {}|{} {} {}\n'
    out = ''
    for i, row in enumerate(X):
        out += tmp.format(*[str(x) for x in row])
        if i in [2, 5]:
            out += '-'*17 + '\n'
    out = out.replace('0', '_')
    return out



class Sudoku(object):
    def __init__(self, X, name=''):
        self.name = name
        self.values = np.array(X)
        self.solvable = True


    def __repr__(self):
        return format_grid(self.values)


    @property
    def mask(self):
        return make_mask(self)



    def square(self, X, Y):
        # returns the values in the 3x3 square encapsulating the value with
        # coordinates x, y
        squarex, squarey = X//3, Y//3
        out = np.zeros([3, 3], dtype=int)
        for i in [0, 1, 2]:
            for j in [0, 1, 2]:
                y = squarey*3 + i
                x = squarex*3 + j
                out[i, j] = self.values[y, x]
        return out.ravel()


    def solved(self):
    # Checks if sudoku puzzle, X, is successfully solved.
        if 0 in self.values:
            return False

        for row in self.values:
            if any(x not in row for x in range(1, 10)):
                return False

        for column in self.values.T:
            if any(x not in column for x in range(1, 10)):
                return False

        for xsquare, ysquare in product([0, 3, 6], [0, 3, 6]):
            if any(x not in self.square(xsquare, ysquare) for x in range(1, 10)):
                return False

        return True

    def valid(self): #!!! This function is expensive!
        for i, j in product(range(9), range(9)):
            if self.values[i, j] != 0:
                continue
            lookthrough = [key for (key, val) in self.mask.items() if val[i, j]==1]
            if len(lookthrough) == 0:
#                print('{}. at (x={}, y={})'.format('invalid', j+1, i+1))
#                print(self)
#                time.sleep(1)
                return False
        return True


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

def fromString(string):
    values = []
    for line in string.split():
        values.append([int(x) for x in line])
    return Sudoku(values)



def toString(X): #!!! this doesnt format the same way as the previous
    out = ''
    for row in X.values:
        out += ''.join([str(i) for i in row]) + '\n'
    return out


def make_mask(X):

    masks = {i:np.ones([9, 9], dtype=int) for i in range(1, 10) }
    for val, mask in masks.items():
        # make mask of possible moves for val

        # iterate over rows:
        for i, row in enumerate(X.values):
            if val in row:
                mask[i, :] = 0
        # iterate over columns:
        for i, col in enumerate(X.values.T):
            if val in col:
                mask[:, i] = 0

        # iterate over squares: (i, j are coords of the top left corner)
        for i, j in product([0, 3, 6], [0, 3, 6]):
            if val in X.square(i, j):
                mask[j:j+3, i:i+3] = 0

        # eliminate filled positions
        for i, j in product(range(9), range(9)):
            if X.values[j, i] !=0:
                mask[j, i] = 0

    return masks


def deduce_move(X, masks):
    for val, mask in masks.items():
        for i, row in enumerate(mask):
            if sum(row) != 1: # ignore rows with no possible move.
                continue
            # TODO: is there a better way of doing this?
            j = [ind for (ind, x) in enumerate(row) if x==1][0]

            return i, j, val, 'row deduction'

        #iterate over columns of mask
        for i, col in enumerate(mask.T):
            if sum(col) != 1: # ignore columns with no possible move.
                continue
            # TODO: is there a better way of doing this?
            j = [ind for (ind, x) in enumerate(col) if x==1][0]
            return j, i, val, 'column deduction'

        # iterate over squares of mask.
        for I, J in product([0, 3, 6], [0, 3, 6]):
            thisSquare = mask[J:J+3, I:I+3]
            if thisSquare.sum() != 1: # ignore squares with no possible move.
                continue
            for ind, row in enumerate(thisSquare):
                if 1 in row:
                    j = J + ind
                    break
            for ind, col in enumerate(thisSquare.T):
                if 1 in col:
                    i = I + ind
                    break
            return j, i, val, 'square deduction'

    # look at each square and through the mask to find only possibilities
    for i, j in product(range(9), range(9)):
        lookthrough = [key for (key, val) in masks.items() if val[i, j]==1]
        if len(lookthrough) == 1:
            return i, j, lookthrough[0], 'no other possibilities'


    return None



def solve_old(X, verbose=False, layer=0):
    # returns the solved sudoku puzzle if it can find a solution. If not, returns
    # None.
    X = deepcopy(X)

    masks = make_mask(X)
    move = deduce_move(X, masks)
    while move:

        i, j, val, desc = move
        if verbose:
            print(X)
            print('{}. {} at (x={}, y={})'.format(desc, val, j+1, i+1))
            print(format_grid(masks[val]))
            time.sleep(1)

        X.values[i, j] = val


        masks = make_mask(X)

        move = deduce_move(X, masks)


    if not X.valid():

        if verbose:
            print('INVALID')
        return None
    if X.solved():
        return X
    elif layer < 2: #guess TWO moves and try to solve again

        for j, i in product(range(9), range(9)):
            if X.values[i, j] != 0:
                continue
            possibilities = [key for (key, val) in masks.items() if val[i, j]==1]
            if len(possibilities) > 2:
                continue
            for p in possibilities:
                X_guess = deepcopy(X)
                X_guess.values[i, j] = p
                if verbose:
                    print('{}. {} at (x={}, y={})'.format('guessing (layer) {}...'.format(layer+1), p, j+1, i+1))
                    time.sleep(1)
                Y_guess = solve(X_guess, verbose=verbose, layer=layer+1)
                if Y_guess:
                    return Y_guess
    return None





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
    filename = 'p096_sudoku.txt'
    now = time.time()
    for i, x in enumerate(sudokuGenerator(filename)):
        #if i==49:
        X = x
        XX, moves = solve(X.values)
        print(XX)
        for move in moves:
            print(move)
    print('Time: ', time.time()-now)
