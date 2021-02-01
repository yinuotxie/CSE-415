'''EightPuzzleWithManhattan.py
This file augments EightPuzzleWithManhattan.py with heuristic information,
so that it can be used by an A* implementation.
'''

from EightPuzzle import *

BOARD = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]


def h(s):
    '''We return the Mahattan distanc'''
    total_dist = 0
    for row in range(3):
        for col in range(3):
            tile = s.b[row][col]
            if tile != 0:
                (b_row, b_col) = (tile//3, tile % 3)    # correct position of tile
                total_dist = total_dist + abs(b_row - row) + abs(b_col - col)
    return total_dist
