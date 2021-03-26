'''Q_Learn.py
STUDENT STARTER TEMPLATE ...

Implement Q-Learning in this file by completing the implementations
of the functions whose stubs are present.
Add or change code wherever you see #*** ADD OR CHANGE CODE HERE ***

This is part of the UW Intro to AI Starter Code for Reinforcement Learning.

'''
from TowersOfHanoi import *
import TowersOfHanoi
import random as rd 
import math 

# Edit the returned name to ensure you get credit for the assignment.
def student_name():
#*** ADD OR CHANGE CODE HERE ***
    return "Travis Xie" # For an autograder.

STATES=None; ACTIONS=None; UQV_callback=None; Q_VALUES=None
is_valid_goal_state=None; Terminal_state = None
USE_EXPLORATION_FUNCTION = None
INITIAL_STATE = None
EXPLORATION_FUNCTION = None
CHANGES = None
STATE_ACTION = {}    # record the times that (s, a) is taken 
LAMBDA = 0.8
K = 20
def setup(states, actions, q_vals_dict, update_q_value_callback,\
    goal_test, terminal, use_exp_fn=False):
    '''This method is called by the GUI the first time a Q_Learning
    menu item is selected. It may be called again after the user has
    restarted from the File menu.
    Q_VALUES starts out with all Q-values at 0.0 and a separate key
    for each (s, a) pair.'''
    global STATES, ACTIONS, UQV_callback, Q_VALUES, is_valid_goal_state
    global USE_EXPLORATION_FUNCTION, Terminal_state
    global CHANGES, STATE_ACTION, EXPLORATION_FUNCTION
    STATES = states
    ACTIONS = actions
    Q_VALUES = q_vals_dict
    UQV_callback = update_q_value_callback
    is_valid_goal_state = goal_test
    Terminal_state = terminal
    USE_EXPLORATION_FUNCTION = use_exp_fn
    CHANGES = 0         # record the number of times that Q_value changes  
    if USE_EXPLORATION_FUNCTION:
        EXPLORATION_FUNCTION = lambda u, n: u + K / n
        for (s, a) in Q_VALUES.keys():
            STATE_ACTION[(s, a)] = 1
        print("An exploration function is implemented")

PREVIOUS_STATE = None
LAST_ACTION = None
def set_starting_state(s):
    '''This is called by the GUI when a new episode starts.
    Do not change this function.'''
    global INITIAL_STATE, PREVIOUS_STATE
    print("In Q_Learn, setting the starting state to "+str(s))
    INITIAL_STATE = s
    PREVIOUS_STATE = s

ALPHA = 0.5
CUSTOM_ALPHA = False
EPSILON = 0.5
CUSTOM_EPSILON = False
GAMMA = 0.9
def set_learning_parameters(alpha, epsilon, gamma):
    ''' Called by the system. Do not change this function.'''
    global ALPHA, EPSILON, CUSTOM_ALPHA, CUSTOM_EPSILON, GAMMA
    ALPHA = alpha
    EPSILON = epsilon
    GAMMA = gamma
    if alpha < 0: CUSTOM_ALPHA = True
    else: CUSTOM_ALPHA = False
    if epsilon < 0: CUSTOM_EPSILON = True
    else: CUSTOM_EPSILON = False

def update_Q_value(previous_state, previous_action, new_value):
    '''Whenever your code changes a value in Q_VALUES, it should
    also call this method, so the changes can be reflected in the
    display.
    Do not change this function.'''
    UQV_callback(previous_state, previous_action, new_value)

def handle_transition(action, new_state, r):
    '''When the user drives the agent, the system will call this function,
    so that you can handle the learning that should take place on this
    transition.'''
    global PREVIOUS_STATE, CHANGES

#*** ADD OR CHANGE CODE HERE ***
    
    # list of q_values of current state
    q_value = [Q_VALUES[(s, a)] for (s, a) in Q_VALUES.keys() if s == new_state]

    sample = r + max(q_value) * GAMMA

    new_qval = (1 - ALPHA) * Q_VALUES[(PREVIOUS_STATE, action)] + \
                     ALPHA * sample 

    # You should call update_Q_value before returning.  E.g.,

    Q_VALUES[(PREVIOUS_STATE, action)] = new_qval

    if new_qval - Q_VALUES[(PREVIOUS_STATE, action)] > 0:
        CHANGES += 1

    update_Q_value(PREVIOUS_STATE, action, new_qval)
    PREVIOUS_STATE = new_state
    print("Transition to state: "+str(new_state)+\
          "\n with reward "+str(r)+" is currently handled by the program.")
    return # Nothing needs to be returned.


def choose_next_action(s, r, terminated=False):
    '''When the GUI or engine calls this, the agent is now in state s,
    and it receives reward r.
    If terminated==True, it's the end of the episode, and this method
    can just return None after you have handled the transition.

    Use this information to update the q-value for the previous state
    and action pair.  
    
    Then the agent needs to choose its action and return that.

    '''
    global INITIAL_STATE, PREVIOUS_STATE, LAST_ACTION, EPSILON, STATE_ACTION

    # Unless s is the initial state, compute a new q-value for the
    # previous state and action.
    if not (s==INITIAL_STATE):
        # Compute the update here.
        handle_transition(LAST_ACTION, s, r)

    # Now select an action according to your Q-Learning criteria, such
    # as expected discounted future reward vs exploration.
    # If EPSILON > 0, or CUSTOM_EPSILON is True,
    # then use epsilon-greedy learning here.
    next_action = ACTIONS[0]
    if is_valid_goal_state(s):
        print("It is a goal state; Exit")
        next_action = "Exit"
    elif s == Terminal_state:
        print("It is not a goal_state. But if it's the special Terminal State, return None")
        next_action = None
    else:
        # get all possible actions for the current state
        action_List = [action for (state, action) in Q_VALUES.keys() 
                            if state == s]

        if USE_EXPLORATION_FUNCTION:
            '''f(u, n) = u + K / n'''
            print("Using Exploration Function")
            best_val = -99
            for a in action_List:
                f = EXPLORATION_FUNCTION(Q_VALUES[(s, a)], STATE_ACTION[(s, a)])
                if f > best_val:
                    best_val = f
                    next_action = a
            STATE_ACTION[(s, next_action)] += 1
        # use epsilon greedy exploration 
        else:
            # generate all possible actions for previous state
            prob = rd.random()
            # if custom epsilon, the probability of exploiting decreases 
            # as searching step increases
            # Exponential Distrubition pr(x) = lambda * exp(-lambda * x)
            # I also set a lower bound for the custom epsilon value
            # to prevent being stuck in the sub-optimal policy
            if CUSTOM_EPSILON:

                e = LAMBDA * math.exp(- LAMBDA * (CHANGES / (10 ^ N_disks)))
                EPSILON = max(e, 0.2)

            # act randomly, explore
            if prob <= EPSILON:
                next_action = rd.choice(action_List)
            # act on current policy, exploit 
            else:
                best_val = -99
                # find the best action 
                for (state, action) in Q_VALUES.keys():
                    if state == s:
                        if Q_VALUES[(state, action)] > best_val:
                            best_val = Q_VALUES[(state, action)]
                            next_action = action


    LAST_ACTION = next_action # remember this for next time
    PREVIOUS_STATE = s
    return next_action

Policy = {}
def extract_policy(S, A):
    '''Return a dictionary mapping states to actions. Obtain the policy
    using the q-values most recently computed.
    Ties between actions having the same (s, a) value can be broken arbitrarily.
    Reminder: goal states should map to the Exit action, and no other states
    should map to the Exit action.
    '''
    global Policy
    Policy = {}
#*** ADD OR CHANGE CODE HERE ***  
# return_Q_values(S, A)

    for (s, a) in Q_VALUES.keys():
        if s not in Policy.keys():
            Policy[s] = a 

        if is_valid_goal_state(s):
            Policy[s] = 'Exit'
        elif s == Terminal_state:
            Policy[s] == None
        else:
            if Q_VALUES[(s, a)] > Q_VALUES[(s, Policy[s])]:
                Policy[s] = a 

    return Policy
