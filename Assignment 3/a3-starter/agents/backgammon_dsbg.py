'''
Name(s):  Susan Yang, Yinuo Xie
UW netid(s): xuanry, yinuox
'''

from game_engine import genmoves

class BackgammonPlayer:
    def __init__(self):
        self.GenMoveInstance = genmoves.GenMoves()
        self.states = 0              # number of states explored
        self.cutoffs = 0             # number of states that is being cutoff
        self.maxply = 3              # max depth
        self.MIN = -100000
        self.MAX = 100000
        self.prune = True            # whether to use alpha-beta pruning 
        self.dict = {}               # dictionary that keep tracks of the best value (key) and its move

    # returns a string representing a unique nick name for your agent
    def nickname(self):
        return "yinuox, xuanry"
       


    # If prune==True, changes the search algorthm from minimax
    # to Alpha-Beta Pruning
    def useAlphaBetaPruning(self, prune=False):
        self.states = 0
        self.cutoffs = 0
        self.prune = prune


    # Returns a tuple containing the number explored
    # states as well as the number of cutoffs.
    def statesAndCutoffsCounts(self):
        return (self.states, self.cutoffs)


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
    def move(self, state, die1=1, die2=6):
        self.dict.clear()                # reset the dictionary for every new move
        value = self.minimax(state, state.whose_move, self.maxply, self.MIN, self.MAX, die1, die2)
        return self.dict[value]


    # Given a state, returns an integer which represents how good the state is
    # for the two players (W and R) -- more positive numbers are good for W
    # while more negative numbers are good for R
    def staticEval(self, state):
        ''' Count the pips counts for white and red player. 
        Fewer pips counts means better
        '''
        red = 0                    # pips counts 
        white = 0
        
        for i in range(24):
            count = 0                    # check how many checker are on the possition
            is_white = False             # whether the cherker is white 
            for checker in state.pointLists[i]:
                if(checker == 0):  
                    is_white = True 
                    count += 1
                    white += (24 - i)           
                else:
                    count += 1
                    red += (i + 1)

            # only one checker on the position
            # might be hit by the opponent checkers in front of it
            if count == 1:
                if is_white:
                    red_front = 0         # record the number of red checker in front of it

                    # the largest value of die is 12 
                    # For example, if the white checker is at 8
                    # it may be hit by any red checker from 9 to 20
                    for j in range(i + 1, min(24, i + 12 + 1)):      
                        if checker == 1:
                            red_front += 1
                    white += 2 * red_front
                else:
                    white_front = 0       # record the number of white checker in front of it
                    for j in range(max(i - 12, 0), i):
                        if checker == 0:
                            white_front += 1
                    red += 2 * white_front


        for checker in state.bar:
            if(checker == 0):
                white = white + 25
            else:
                red = red + 25
        
        red -= 25 * len(state.red_off)
        white -= 25 * len(state.white_off)

        # return the difference
        # more positive means good for white (white gets closer to win)
        # negative means good for red (red gets closer to win)
        return red - white


    def minimax(self, state, whoseMove, plyLeft, alpha, beta, die1, die2):
        ''' minmax search. Search for the best move and its correspoding staticEval
        for the current state and the current player (whoseMove)
        return a paire of (moove, value)
        '''
        if plyLeft == 0:        
            return self.staticEval(state)

        if whoseMove == 0:  
            bestVal = self.MIN
        else:
            bestVal = self.MAX

        bestMove = None
        move_state_list = self.get_all_possible_moves_state(state, die1, die2)
        non_cut_off = 0    # record the number of states that are not cut off
        for (m, s) in move_state_list:
            non_cut_off += 1      
            self.states += 1
            newVal = self.minimax(s, s.whose_move, plyLeft - 1, alpha, beta, die1, die2)
            if (whoseMove == 0 and newVal > bestVal) or \
                (whoseMove == 1 and newVal < bestVal):                  
                bestVal = newVal
                bestMove = m 

            # alpha beta pruning 
            if self.prune:
                if whoseMove == 0:
                    alpha = max(alpha, bestVal)
                else:
                    beta = min(beta, bestVal)

                if alpha >= beta:
                    self.cutoffs = self.cutoffs + len(move_state_list) - non_cut_off
                    break 

        self.dict[bestVal] = bestMove
        return bestVal


    def get_all_possible_moves_state(self, state, die1, die2):
        """Uses the mover to generate all legal (moves, state). Returns an array of tuples"""
        # reset the move_generator to every new state passed in
        move_generator = self.initialize_move_gen_for_state(state, state.whose_move, die1, die2)
        move_state_list = []
        done_finding_moves = False
        any_non_pass_moves = False
        while not done_finding_moves:
            try:
                m = next(move_generator)         # Gets a (move, state) pair.        
                if m[0] != 'p':                          
                    any_non_pass_moves = True          
                    move_state_list.append(m)    # Add the (move, state) to the list.
            except StopIteration as e:
                done_finding_moves = True
        if not any_non_pass_moves:                  # if no move, then the state doesn't change
            move_state_list.append(('p', state))    
        return move_state_list
