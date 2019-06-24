# https://python-packaging.readthedocs.io
from setuptools import setup

setup(name                 = 'Sudoku_solver',
      version              = '0.1',
      description          = 'A Sudoku solver with CLI',
      #url                  = '',
      author               = 'Jaime Liew',
      author_email         = 'jyli@dtu.dk',
      license              = 'MIT',
      packages             = ['Sudoku'],
      install_requires     = ['click', 'termcolor'],
      zip_safe             = False,
      include_package_date = True,
      entry_points         = {'console_scripts':
                              ['sudoku=Sudoku.cli:cli']}

)
