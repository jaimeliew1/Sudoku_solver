import click
import Sudoku

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
    if file:
        with open(file) as f:
            X = Sudoku.fromString(f.read(), empty=sep)
    elif from_string:
        X = Sudoku.fromString(from_string, empty=sep)
    X_solved, _ = Sudoku.solve(X)

    print(Sudoku.format_sudoku(X))
    print(Sudoku.format_sudoku(X_solved))

@cli.command()
@click.option('--file', '-f', type=click.Path(exists=True))
@click.option('--from_string', '-s', type=str)
@click.option('-sep', type=str, default='_')
def hint(file=None, from_string=None, sep='_'):
    '''
    Provides the next best move for a given sudoku puzzle.
    '''
    click.echo('hint called')
    if file:
        with open(file) as f:
            X = Sudoku.fromString(f.read(), empty=sep)
    elif from_string:
        X = Sudoku.fromString(from_string, empty=sep)
    X_solved, moves = Sudoku.solve(X)

    print(Sudoku.format_sudoku(X))
    move = moves[0]
    print(f'put {move[0]} at location ({move[2]+1}, {move[1]+1}).')
