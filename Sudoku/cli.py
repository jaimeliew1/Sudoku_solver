import click
import Sudoku
import numpy as np

@click.group()
def cli():
    pass


@cli.command()
@click.option('--file', '-f', type=click.Path(exists=True))
@click.option('--from_string', '-s', type=str)
@click.option('-sep', type=str, default='_')
def solve(file=None, from_string=None, sep='_'):
    '''
    solves a given sudoku puzzle.
    '''
    click.echo('solve called')
    solve_and_print(file, from_string, sep, n=100)



@cli.command()
@click.option('--file', '-f', type=click.Path(exists=True))
@click.option('--from_string', '-s', type=str)
@click.option('-sep', type=str, default='_')
@click.option('-n', type=int, default=1)
def hint(file=None, from_string=None, sep='_', n=1):
    '''
    Provides the next best move for a given sudoku puzzle.
    '''
    click.echo('hint called')
    solve_and_print(file, from_string, sep, n)




def solve_and_print(file=None, from_string=None, sep='_', n=1):
    if file:
        with open(file) as f:
            X = Sudoku.fromString(f.read(), empty=sep)
    elif from_string:
        X = Sudoku.fromString(from_string, empty=sep)
    X_solved, moves = Sudoku.solve(X)

    mask = np.zeros([9, 9])
    for i in range(min(n, len(moves))):
        move = moves[i]
        mask[move[1], move[2]] = 1
        X[move[1], move[2]] = move[0]
    Sudoku.print_sudoku(X, mask)
