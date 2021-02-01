''' AStar.py
by Jia-Jia (Jay) Lin
UWNetID: jial8
Student number: 1820474
Assignment 2, in CSE 415, Winter 2020.
This file contains my AStar implementation.
'''

VERBOSE = False  # Set to True to see progress; but it slows the search.

import sys

if sys.argv==[''] or len(sys.argv)<2:
  # import EightPuzzle as Problem
  import FranceWithDXHeuristic as Problem
  #import EightPuzzleWithHamming as Problem
  #import EightPuzzleWithManhattan as Problem
else:
  import importlib
  Problem = importlib.import_module(sys.argv[1])

print("\nWelcome to AStar!")

COUNT = None # Number of nodes expanded.
MAX_OPEN_LENGTH = None # How long OPEN ever gets.
SOLUTION_PATH = None # List of states from initial to goal, along lowest-cost path.
TOTAL_COST = None # Sum of edge costs along the lowest-cost path.
BACKLINKS = {} # Predecessor links, used to recover the path.
h = Problem.h # Heuristic function from Problem

f = {} # global hash table to associate f values with states.

class My_Priority_Queue:
  def __init__(self):
    self.q = [] # Actual data goes in a list.
  def __contains__(self, elt):
    for pair in self.q:
      if pair[0]==elt: return True
    return False
  def delete_min(self):
    ''' Standard priority-queue dequeuing method.'''
    if self.q==[]: return [] 
    temp_min_pair = self.q[0]
    temp_min_value = temp_min_pair[1]
    temp_min_position = 0
    for j in range(1, len(self.q)):
      if self.q[j][1] < temp_min_value:
        temp_min_pair = self.q[j]
        temp_min_value = temp_min_pair[1]  
        temp_min_position = j
    del self.q[temp_min_position]
    return temp_min_pair
  def insert(self, state, priority):
    if self[state] != -1:
      #print("Error: You're trying to insert an element into a My_Priority_Queue instance,")
      #print(" but there is already such an element in the queue.")
      return
    self.q.append((state, priority))
  def __len__(self):
    '''We define length of the priority queue to be the
    length of its list.'''
    return len(self.q)
  def __getitem__(self, state):
    '''This method enables Pythons right-bracket syntax.
    Here, something like  priority_val = my_queue[state]
    becomes possible. Note that the syntax is actually used
    in the insert method above:  self[state] != -1  '''
    for (S,P) in self.q:
      if S==state: return P
    return -1  
  def __delitem__(self, state):
    '''This method enables Python's del operator to delete
    items from the queue.'''
    #print("In MyPriorityQueue.__delitem__: state is: ", str(state))
    for count, (S,P) in enumerate(self.q):
      if S==state:
        del self.q[count]
        return
  def __str__(self):
    "Code to create a string representation of the PQ."
    txt = "My_Priority_Queue: ["
    for (s,p) in self.q: txt += '('+str(s)+','+str(p)+') '
    txt += ']'
    return txt

def runAStar():
  initial_state = Problem.CREATE_INITIAL_STATE()
  print("Initial State:")
  print(initial_state)
  global COUNT, BACKLINKS, MAX_OPEN_LENGTH, SOLUTION_PATH
  COUNT = 0
  BACKLINKS = {}
  MAX_OPEN_LENGTH = 0
  SOLUTION_PATH = AStar(initial_state)
  print(str(COUNT)+" states expanded.")
  print('MAX_OPEN_LENGTH = '+str(MAX_OPEN_LENGTH))

def AStar(initial_state):
  '''AStar Search algorithm.'''
  global f, COUNT, BACKLINKS, MAX_OPEN_LENGTH, CLOSED, TOTAL_COST, h
  CLOSED = []
  BACKLINKS[initial_state] = None

# STEP 1a. Compute starting f
  OPEN = My_Priority_Queue()
  OPEN.insert(initial_state, 0)
  f[initial_state]= 0.0

# STEP 2. If OPEN is empty, output “DONE” and stop.
  while len(OPEN)>0:
    if VERBOSE: report(OPEN, CLOSED, COUNT)
    if len(OPEN)>MAX_OPEN_LENGTH: MAX_OPEN_LENGTH = len(OPEN)

# STEP 3. Find and remove the item [s,p] on OPEN with lowest p.
#         Put [s,p] on CLOSED.
#         If S is a goal state, output its description
#         (and backtrace a path)
# Note: print(S) shows the name of the city
    (S,P) = OPEN.delete_min()
    #print("OPEN.delete_min chose (S,P)= ", (str(S), P))
    CLOSED.append(S)
    if Problem.GOAL_TEST(S):
      print(Problem.GOAL_MESSAGE_FUNCTION(S))
      path = backtrace(S)
      print('Length of solution path: '+str(len(path)-1)+' edges')
      TOTAL_COST = f[S]
      print('Total cost of solution path: '+str(TOTAL_COST))
      return path
    COUNT += 1

# STEP 4. Generate the list L of [s',f'] pairs where the s' are the
#   successors of s and their f values = f+h
    fs = f[S]
    for op in Problem.OPERATORS:
      if op.precond(S):
        new_state = op.state_transf(S)
        # When checking the CLOSED list, don't necessarily delete the new
        #   state if the same city is already on CLOSED.
        #   If new state has a lower priority than the older one, del state on CLOSED
        #   and put the new_state on OPEN.
        edge_cost = S.edge_distance(new_state)
        new_f = fs + edge_cost
        
        new_f_with_h = new_f + h(new_state)
        if new_state in CLOSED:
            if new_f_with_h < f[new_state] + h(new_state):
                #print("new_state has a lower priority than the old one, del")
                OPEN.insert(new_state, new_f_with_h)
                del CLOSED[CLOSED.index(new_state)]
            else:
              del new_state
            continue
        # If new_state already exists on OPEN:
        #   If its new priority is less than its old priority,
        #     update its priority on OPEN, and set its BACKLINK to S.
        if new_state in OPEN:
          #print("new_state is in OPEN already, so...")
          P = OPEN[new_state]
          if new_f_with_h < P:
            #print("New priority value is lower, so del older one")
            del OPEN[new_state]
            OPEN.insert(new_state, new_f_with_h)
          else:
            #print("Older one is better, so del new_state")
            del new_state
            continue
        else:
            #print("new_state was not on OPEN at all, so just put it on.")
            OPEN.insert(new_state, new_f_with_h)
        BACKLINKS[new_state] = S
        f[new_state] = new_f
    #print_state_queue("OPEN", OPEN)
  # STEP 6. Go to Step 2.
  return None  # No more states on OPEN, and no goal reached.

def print_state_queue(name, q):
  print(name+" is now: ",end='')
  print(str(q))

def backtrace(S):
  global BACKLINKS
  path = []
  while S:
    path.append(S)
    S = BACKLINKS[S]
    #print(S)
  path.reverse()
  print("Solution path: ")
  for s in path:
    print(s)
    #print(f[s])
  return path
  
def report(open, closed, count):
  print("len(OPEN)="+str(len(open)), end='; ')
  print("len(CLOSED)="+str(len(closed)), end='; ')
  print("COUNT = "+str(count))

if __name__=='__main__':
  runAStar()