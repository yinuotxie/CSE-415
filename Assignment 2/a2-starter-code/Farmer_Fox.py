'''Farmer_Fox.py
by Travis Xie
UWNetID: yinuox
Student number: 1864724

Assignment 2 Part 1, in CSE 415, Winter 2021.
 
This file contains my problem formulation for the problem of
the Farmer, Fox, Chicken, and Grain.
'''

#<METADATA>
SOLUTION_VERSION = "1.0"
PROBLEM_NAME = "Farmer, Fox, Chicken, and Grain"
PROBLEM_VERSION = "1.0"
PROBLEM_AUTHORS = ['Travis Xie']
PROBLEM_CREATION_DATE = "19-JAN-2021"

# The following field is mainly for the human solver, via either the Text_SOLUZION_Client.
# or the SVG graphics client.
PROBLEM_DESC=\
 '''The <b>"Farmer, Fox, Chicken, and Grain"</b> problem is a traditional puzzle
in which the player starts off a farmer, a fox, a chicken, and a bag of grain.  
The object is to execute a sequence of legal moves that transfers them all to 
the right bank of the river. In this version, the farmer can only take one of 
the three items in the boat with him at one time. The fox must never be left alone 
with the chicken, and the chicken must never be left alone with the grain. Besides, 
farmer must be presented on the boat to steer the boat. In the formulation presented here, 
the computer will not let you make a move to such a forbidden situation,and 
it will only show you moves that could be executed "safely."
'''
#</METADATA>

#<COMMON_DATA>
#</COMMON_DATA>

#<COMMON_CODE>
FA=0  # array index to access where the farmer is
FO=1  # same idea for fox
C=2   # same idea for chicken
G=3   # same idea for grain
LEFT=0 # use integer to represent left side of the river
RIGHT=1 # same
'''For example, [1, 0, 1, 0] means that farmer, chicken is on the right side
and fox and grain is on the left side
'''

class State():
    def __init__(self, d=None):
        if d==None:
            # initial state where all are on the left side of river
            # 0: left; 1: right
            d = {'people': [0,0,0,0],
                'boat':LEFT}
        self.d = d

    def __eq__(self,s2):
        for prop in ['people', 'boat']:
            if self.d[prop] != s2.d[prop]: 
                return False
        return True

    def __str__(self):
        # Produces a textual description of a state.
        p = self.d['people']
        txt = "\n Farmer is on "+ self.__side__(p, FA) + "\n"
        txt += " Fox is on " + self.__side__(p, FO) +"\n"
        txt += " Chicken is on " + self.__side__(p, C) +"\n"
        txt += " Grain is on " + self.__side__(p, G) +"\n"
        side='left'
        if self.d['boat']==1: 
            side='right'
        txt += " Boat is on the "+side+".\n"
        return txt

    def __side__(self, p, ob):
        # return the side of the given object
        if p[ob] == 0:
            return 'left'
        return 'right'

    def __hash__(self):
        return (self.__str__()).__hash__()

    def copy(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        news = State({})
        news.d['people'] = [i for i in self.d['people']]
        news.d['boat'] = self.d['boat']
        return news 

    def can_move(self,p1,p2):
        '''Tests whether it's legal to move the boat and take
        p1 and p2 to the other side'''
        side = self.d['boat'] # Where the boat is.
        p = self.d['people']
        # farmer and the object he takes with has to be on the same side with boat
        if p[p1] != side or p[p2] != side: return False    

        # check who will be left 
        others = [i for i in [1, 2, 3] if p[i] == side and i != p2]
        if len(others) >=2 :
            # cannot leave fox and chicken together
            if others[0] == 1 and others[1] == 2: return False
            # cannot leave chicken and grain together
            if others[0] == 2 and others[1] == 3: return False
    
        return True


    def move(self,p1,p2):
        '''Assuming it's legal to make the move, this computes
        the new state resulting from moving the boat carrying
        m missionaries and c cannibals.'''
        news = self.copy()    # start with a deep copy.
        side = self.d['boat']         # where is the boat?
        p = news.d['people']          # get the array of positions of people.
        p[p1] = 1 - side              # move p1 to the other side
        if p2 != 0:
            p[p2] = 1 - side          # move p2 to the other side
        news.d['boat'] = 1-side       # Move the boat itself.
        return news

def goal_test(s):
    '''If all are on the right side of the river'''
    p = s.d['people']
    for i in p:
        if i != 1: return False
    return True

def goal_message(s):
    return "Congratulations on successfully guiding the farmer, fox, chicken, and grain across the river!"

class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)
#</COMMON_CODE>

#<INITIAL_STATE>
CREATE_INITIAL_STATE = lambda : State(d={'people':[0,0,0,0], 'boat':LEFT })
#</INITIAL_STATE>

#<OPERATORS>
'''O: farmer; 1: fox; 2: chicken; 3: grain; -1: none
(0, -1): farmer crosses the river alone
(0, 1): farmer crosses the river with the fox
etc.
'''
Move_combinations = [(0,0), (0,1), (0,2), (0,3)]

def name(p2):
    if p2 == 0:
        return 'Farmer crosses the river alone'
    if p2 == 1:
        return 'Farmer crosses the river with fox'
    if p2 == 2:
        return 'Farmer crosses the river with chicken'
    if p2 == 3:
        return 'Farmer crosses the river with grain'

OPERATORS = [Operator(
    name(p2),
    lambda s, p1=p1, p2=p2: s.can_move(p1,p2),
    lambda s, p1=p1, p2=p2: s.move(p1,p2) ) 
    for (p1,p2) in Move_combinations]

#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>

