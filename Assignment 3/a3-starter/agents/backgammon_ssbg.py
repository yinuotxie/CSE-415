'''
Name(s):
UW netid(s):
'''

from game_engine import genmoves

class BackgammonPlayer:
    def __init__(self):
        self.GenMoveInstance = genmoves.GenMoves()
        # TODO: feel free to create more instance variables as needed.

    # returns a string representing a unique nick name for your agent
    def nickname(self):
        # TODO: return a unique nick name for your agent
        return ""

    # Given a ply, it sets a maximum for how far an agent
    # should go down in the search tree. If maxply==-1,
    # no limit is set
    def setMaxPly(self, maxply=-1):
        # TODO: set the max ply
        pass

    # If not None, it update the internal static evaluation
    # function to be func
    def useSpecialStaticEval(self, func):
        # TODO: update your staticEval function appropriately
        pass

    # Given a state and a roll of dice, it returns the best move for
    # the state.whose_move
    def move(self, state, die1, die2):
        # TODO: return a move for the current state and for the current player.
        # Hint: you can get the current player with state.whose_move
        return None


    # Given a state, returns an integer which represents how good the state is
    # for the two players (W and R) -- more positive numbers are good for W
    # while more negative numbers are good for R
    def staticEval(self, state):
        # TODO: return a number for the given state
        return -1
