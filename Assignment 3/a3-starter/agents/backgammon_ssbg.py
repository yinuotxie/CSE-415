'''
Name(s):
UW netid(s):
'''

from game_engine import genmoves


class BackgammonPlayer:
    def __init__(self):
        self.GenMoveInstance = genmoves.GenMoves()
        self.maxply = 2
        self.MIN = -100000
        self.MAX = 100000
        self.dict = {}               # dictionary that keep tracks of the best value and its move
        self.dice = []
        for i in range(1, 7):
            for j in range(1, 7):
                self.dice.append((i, j))

    # returns a string representing a unique nick name for your agent
    def nickname(self):
        # TODO: return a unique nick name for your agent
        return "yinuox, xuanry"

    # Given a ply, it sets a maximum for how far an agent
    # should go down in the search tree. If maxply==-1,
    # no limit is set
    def setMaxPly(self, maxply=-1):
        if maxply != -1:
            self.maxply = maxply

    # If not None, it update the internal static evaluation
    # function to be func
    def useSpecialStaticEval(self, func=None):
        if func is not None:
            self.staticEval = func

    def initialize_move_gen_for_state(self, state, who, die1, die2):
        return self.GenMoveInstance.gen_moves(state, who, die1, die2)

    # Given a state and a roll of dice, it returns the best move for
    # the state.whose_move

    def move(self, state, die1, die2):
        self.dict = {}                  # reset the dictionary for every move
        value = self.expectiminimax(state, state.whose_move, self.maxply, die1, die2)
        return self.dict[value]

    # Given a state, returns an integer which represents how good the state is
    # for the two players (W and R) -- more positive numbers are good for W
    # while more negative numbers are good for R

    def staticEval(self, state):
        red = 0
        white = 0

        for i in range(24):
            for checker in state.pointLists[i]:
                if(checker == 0):
                    white += (24 - i)
                else:
                    red += (i + 1)

        for checker in state.bar:
            if(checker == 0):
                white = white + 25
            else:
                red = red + 25

        red -= 25 * len(state.red_off)
        white -= 25 * len(state.white_off)
        return red - white

    def expectiminimax(self, state, whoseMove, plyLeft, die1, die2):
        if plyLeft == 0:
            return self.staticEval(state)

        if whoseMove == 0:            # maximizing agent
            bestVal = self.MIN
            bestMove = None
            move_state_list = self.get_all_possible_moves_state(state, die1, die2)
            for (m, s) in move_state_list:
                val = 0
                for (dice1, dice2) in self.dice:
                    newVal = self.expectiminimax(s, s.whose_move, plyLeft - 1, dice1, dice2)
                    val += newVal / 36
                    
                if val > bestVal:
                    bestVal = val
                    bestMove = m

            self.dict[bestVal] = bestMove
            return bestVal
            
        else:
            bestVal = self.MAX
            bestMove = None
            move_state_list = self.get_all_possible_moves_state(state, die1, die2)
            for (m, s) in move_state_list:
                val = 0
                for (dice1, dice2) in self.dice:
                    newVal = self.expectiminimax(s, s.whose_move, plyLeft - 1, dice1, dice2)
                    val += 1/36 * newVal
                    
                if val < bestVal:   
                    bestVal = val
                    bestMove = m

            self.dict[bestVal] = bestMove
            return bestVal

    '''
    def expectiminimax(self, state, whoseMove, plyLeft, die1, die2):

        if plyLeft == 0:
            return self.staticEval(state)

        if whoseMove == 0:            # maximizing agent
            bestVal = self.MIN
            bestMove = None
            for (die1, die2) in self.dice:
                # move_state_list = self.get_all_possible_moves_state(state, die1, die2)
                # for (m, s) in move_state_list:
                newVal = self.expectiminimax(state, -1, plyLeft - 1, die1, die2)
                if bestVal > newVal:
                    bestVal = newVal
                    bestMove = m  # determine the best move here
            self.dict[bestVal] = bestMove
            return bestVal
            # // Return value of maximum-valued child node
            # let α := -∞
            # foreach child of node
            # α := max(α, expectiminimax(child, depth-1))
        elif whoseMove == 1:         # mininizing agent
            bestVal = self.MAX
            bestMove = None
            for (die1, die2) in self.dice:
                # move_state_list = self.get_all_possible_moves_state(state, die1, die2)
                # for (m, s) in move_state_list:
                newVal = self.expectiminimax(state, -1, plyLeft - 1, die1, die2)
                if bestVal < newVal:
                    bestVal = newVal
                    bestMove = m
            self.dict[bestVal] = bestMove
            return bestVal
        else:                           # random agent (圆圈)
            # Return weighted average of all child nodes' values
            bestVal = 0
            move_state_list = self.get_all_possible_moves_state(state, die1, die2)
            for (m, s) in move_state_list:
                bestVal += (1/36) * self.expectiminimax(s, s.whose_move, plyLeft - 1, die1, die2)
            # pick a move randomly? will never pick
            return bestVal
    '''

    def get_all_possible_moves_state(self, state, die1, die2):
        """Uses the mover to generate all legal (moves, state). Returns an array of tuples"""
        move_generator = self.initialize_move_gen_for_state(
            state, state.whose_move, die1, die2)
        move_state_list = []
        done_finding_moves = False
        any_non_pass_moves = False
        while not done_finding_moves:
            try:
                m = next(move_generator)         # Gets a (move, state) pair.
                # print("next returns: ", m[0], 'who: ', state.whose_move, 'plyLeft: ', plyLeft)          # Prints out the move.    For debugging.
                if m[0] != 'p':
                    any_non_pass_moves = True
                    # Add the (move, state) to the list.
                    move_state_list.append(m)
            except StopIteration as e:
                done_finding_moves = True
        if not any_non_pass_moves:
            move_state_list.append(('p', state))
        return move_state_list
