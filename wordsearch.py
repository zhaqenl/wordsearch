"""
This script is for handling specialized wordsearch input files.

The format for the input file is the following:

'Number of cases'
'String grid height'
'String grid width'
'String grid'
'Word to find'
...
...
...

Simply run:

python wordsearch.py `input_file.txt`
"""


import sys
import argparse
import core

PARSER = argparse.ArgumentParser()
PARSER.add_argument('filename')
ARGS = PARSER.parse_args()

with open(ARGS.filename) as f:
    CASE_COUNT = f.readline().strip('\n')
    for case in xrange(int(CASE_COUNT)):
        sys.stdout.write('Case ')
        sys.stdout.write(str(case + 1))
        sys.stdout.write(': ')
        grid = []
        grid_height_limit = int(f.readline().strip('\n'))
        grid_width = int(f.readline().strip('\n'))
        for _ in xrange(grid_height_limit):
            grid += [f.readline().strip('\n')]
        word = f.readline().strip('\n')
        print core.wordsearch(word, grid)
    sys.stdout.flush()
