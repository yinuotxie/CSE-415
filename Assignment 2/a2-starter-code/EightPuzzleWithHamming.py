'''EightPuzzleWithHamming.py
This file augments EightPuzzleWithHamming.py with heuristic information,
so that it can be used by an A* implementation.
Hamming Distance: count the number of tiles out of place, but not the blank
'''

from EightPuzzle import *

BOARD = [[0, 1, 2],[3, 4, 5],[6, 7, 8]]

def h(s):
    '''We return the number of tiles out of place'''
    count = 0
    for row in range(3):
        for col in range(3): 
            if BOARD[row][col] != s.b[row][col] and s.b[row][col] != 0:
                count += 1
    return count