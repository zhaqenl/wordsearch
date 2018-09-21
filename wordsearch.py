"""

"""


import core
import input_data
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

with open(args.filename) as f:
    case_count = f.readline().strip('\n')
    for case in xrange(int(case_count)):
        print 'Case ' + str(case + 1) + ': ',
        grid = []
        grid_height_limit = int(f.readline().strip('\n'))
        grid_width = int(f.readline().strip('\n'))
        for _ in xrange(grid_height_limit):
            grid += [f.readline().strip('\n')]
        word = f.readline().strip('\n')
        print core.wordsearch(word, grid)
