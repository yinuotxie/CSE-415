'''
Name(s):  Susan Yang, Travis Xie
UW netid(s): xuanry, yinuox
'''
'''
One die has all ones and the other has all sixes
Also need two counter variables. 
One is used to count the numbe of states created by the agent 
The other is used to count the number Alpha-Beta cutoffs 
(from whenever this counter is most recently reset)
'''
from game_engine import genmoves

class BackgammonPlayer:
    def __init__(self):
        self.GenMoveInstance = genmoves.GenMoves()
        self.states = 0
        self.cutoffs = 0
        self.maxply = 3
        self.MIN = -100000
        self.MAX = 100000
        self.funct = lambda state: self.f(state)
        self.prune = False

    # returns a string representing a unique nick name for your agent
    def nickname(self):
        #return a string representation of your UW netid(s)
        return "yinuox, xuanry"

    # If prune==True, changes the search algorthm from minimax
    # to Alpha-Beta Pruning
    def useAlphaBetaPruning(self, prune=False):
        # use the prune flag to indiciate that your search
        # should use Alpha-Beta rather than minimax
        self.states = 0
        self.cutoffs = 0
        self.prune = prune

    # Returns a tuple containing the number explored
    # states as well as the number of cutoffs.
    def statesAndCutoffsCounts(self):
        # return a tuple containig states and cutoff
        return (self.states, self.cutoffs)

    # Given a ply, it sets a maximum for how far an agent
    # should go down in the search tree. If maxply==-1,
    # no limit is set
    def setMaxPly(self, maxply=-1):
        # set the max ply
        if maxply != -1:
            self.maxply = maxply

    # If not None, it update the internal static evaluation
    # function to be func
    def useSpecialStaticEval(self, func=None):
       if func is not None:
           self.funct = func


    # Given a state and a roll of dice, it returns the best move for
    # the state.whose_move
    def move(self, state, die1=1, die2=6):
        self.move_generator = self.GenMoveInstance.gen_moves(state, state.whose_move, die1, die2)

        return self.minimax(state, 'p', state.whose_move, self.maxply, self.MIN, self.MAX)[0]    #(move, provisional)


    # Given a state, returns an integer which represents how good the state is
    # for the two players (W and R) -- more positive numbers are good for W
    # while more negative numbers are good for R
    def staticEval(self, state):
        return self.funct(state)

    # static evalulation function, counting pips 
    # less pips mean less move needed to finish the game
    # see https://bkgm.com/articles/Driver/GuideToCountingPips/ 
    def f(self, state):
        red = 0
        white = 0
        
        for i in range(len(state.pointLists)):
            for piece in state.pointLists[i]:
                # the closer the piece gets to the home, the more value it gains
                if(piece == "W"):    
                    white += (24 - i)               
                else:
                    red += i
            
        for piece in state.bar:
            if(piece == 'W'):
                white = white - 24
            else:
                red = red - 24
        
        red += 25 * len(state.red_off)
        white += 25 * len(state.white_off)

        return red - white

    # W = 0
    # R = 1
    # minmax search, return (move, value)
    def minimax(self, state, move, whoseMove, plyLeft, alpha, beta):
        ''' minmax search. Search for the best move and its correspoding staticEval
        for the current state and the current player (whoseMove)
        return a paire of (moove, value)
        '''
        if plyLeft == 0:
            return (move, staticEval(state))

        if whoseMove == 0:  
            provisional = self.MIN
            for (m, s) in self.get_all_possible_moves_state():
                self.states += 1          # increment 1 for each state explored
                (newMove, newVal) = self.minimax(s, m, 1 - whoseMove, plyLeft-1, alpha, beta)    # iterative method
                # if there is a better option, update the pair
                if newVal > provisional:                  
                    (move, provisional) = (newMove, newVal)

            # using alpha beta pruning 
                if self.prune:
                    alpha = max(alpha, provisional)
                    if alpha >= beta:
                        self.cutoffs += 1
                        break
            return (move, provisional)  
        
        else:               
            provisional = self.MAX
            
            for (m, s) in self.get_all_possible_moves_state():
                self.states += 1          # increment 1 for each state explored
                (newMove, newVal) = self.minimax(s, m, 1 - whoseMove, plyLeft-1, alpha, beta)    # iterative method
                # if there is a better option, update the pair
                if newVal < provisional:                  
                    (move, provisional) = (newMove, newVal)

            # using alpha beta pruning 
                if self.prune:
                    beta = min(beta, provisional)
                    if alpha >= beta:
                        self.cutoffs += 1
                        break
        
            return (move, provisional)  

    
    def get_all_possible_moves_state(self):
        """Uses the mover to generate all legal (moves, state). Returns an array of tuples"""
        move_state_list = []
        done_finding_moves = False
        while not done_finding_moves:
            try:
                (m, s) = next(self.move_generator)    # Gets a (move, state) pair.
                if m != 'p':                          # legal move
                    move_state_list.append((m, s))    # Add the (move, state) to the list.
            except StopIteration as e:
                done_finding_moves = True
        return move_state_list
    