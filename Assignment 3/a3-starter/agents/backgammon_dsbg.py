'''
Name(s):  Susan Yang, Yinuo Xie
UW netid(s): xuanry, yinuox
'''

from game_engine import genmoves

class BackgammonPlayer:
    def __init__(self):
        self.GenMoveInstance = genmoves.GenMoves()
        self.GenMoveInstance = genmoves.GenMoves()
        self.states = 0
        self.cutoffs = 0
        self.maxply = 3
        self.MIN = -100000
        self.MAX = 100000
        self.prune = True
        self.dict = {}               # dictionary that keep tracks of the best value and its move

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
        self.dict = {}                  # reset the dictionary for every move
        value = self.minimax(state, state.whose_move, self.maxply, self.MIN, self.MAX, die1, die2)
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

    def minimax(self, state, whoseMove, plyLeft, alpha, beta, die1, die2):
        ''' minmax search. Search for the best move and its correspoding staticEval
        for the current state and the current player (whoseMove)
        return a paire of (moove, value)
        '''
        if plyLeft == 0:
            return self.staticEval(state)

        if whoseMove == 0:  
            bestVal = self.MIN
            bestMove = None
            move_state_list = self.get_all_possible_moves_state(state, die1, die2, plyLeft)
            non_cut_off = 0  
            for (m, s) in move_state_list:
                non_cut_off += 1
                self.states += 1
                newVal = self.minimax(s, s.whose_move, plyLeft - 1, alpha, beta, die1, die2)
                if newVal > bestVal:                  
                    bestVal = newVal
                    bestMove = m 

                if self.prune:
                    alpha = max(alpha, bestVal)
                    if alpha >= beta:
                        self.cutoffs = self.cutoffs + len(move_state_list) - non_cut_off
                        break 

            self.dict[bestVal] = bestMove
            return bestVal
        else:
            bestVal = self.MAX
            move_state_list = self.get_all_possible_moves_state(state, die1, die2, plyLeft)
            non_cut_off = 0  
            for (m, s) in move_state_list:
                non_cut_off += 1
                self.states += 1
                newVal = self.minimax(s, 1 - whoseMove, plyLeft - 1, alpha, beta, die1, die2)
                if newVal < bestVal:                  
                    bestVal = newVal
                    bestMove = m

                # using alpha beta pruning 
                if self.prune:
                    beta = min(beta, bestVal)
                    if alpha >= beta:
                        self.cutoffs = self.cutoffs + len(move_state_list) - non_cut_off
                        break

            self.dict[bestVal] = bestMove
            return bestVal

    def get_all_possible_moves_state(self, state, die1, die2, plyLeft):
        """Uses the mover to generate all legal (moves, state). Returns an array of tuples"""
        move_generator = self.initialize_move_gen_for_state(state, state.whose_move, die1, die2)
        move_state_list = []
        done_finding_moves = False
        any_non_pass_moves = False
        while not done_finding_moves:
            try:
                m = next(move_generator)         # Gets a (move, state) pair.
                #print("next returns: ", m[0], 'who: ', state.whose_move, 'plyLeft: ', plyLeft)          # Prints out the move.    For debugging.
                if m[0] != 'p':                          
                    any_non_pass_moves = True          
                    move_state_list.append(m)    # Add the (move, state) to the list.
            except StopIteration as e:
                done_finding_moves = True
        if not any_non_pass_moves:
            move_state_list.append(('p', state))
        return move_state_list
