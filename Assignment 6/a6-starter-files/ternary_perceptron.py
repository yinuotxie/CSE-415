'''ternary_perceptron.py
Complete this python file as part of Part B.
You'll be filling in with code to implement:

a 3-way classifier
a 3-way weight updater

This program can be run from the given Python program
called run_3_class_4_feature_iris_data.py.

 
'''
def student_name():
  return "Travis Xie" # Replace with your own name.
  

def classify(W, x_vector):
  '''Assume W = [W0, W1, W2] where each Wi is a vector of
     weights = [w_0, w_1, ..., w_{n-1}, biasweight]
     Assume x_vector = [x_0, x_1, ..., x_{n-1}]
       Note that y (correct class) is not part of the x_vector.
     Return 0, 1, or 2,
       depending on which weight vector gives the highest
       dot product with the x_vector augmented with the 1 for bias
       in position n.
  '''
  #ADD YOUR CODE HERE
  y_list = []
  for weight in W:
    # add the bias
    y = weight[-1] * 1
    for i in range(len(x_vector)):
      y += weight[i] * x_vector[i]
    y_list.append(y)

  return argmax(y_list)

# Helper function for finding the arg max of elements in a list.
# It returns the index of the first occurrence of the maximum value.
def argmax(lst):
  idx, mval = -1, -1E20
  for i in range(len(lst)):
    if lst[i]>mval:
      mval = lst[i]
      idx = i
  return idx

def train_with_one_example(W, x_vector, y, alpha):
  '''Assume weights are as in the above function classify.
     Also, x_vector is as above.
     Here y should be 0, 1, or 2, depending on which class of
     irises the example belongs to.
     Learning is specified by alpha.
  '''
  # ADD YOUR CODE HERE
  y_prime = classify(W, x_vector)

  if y_prime == y:
    return (W, False)
  # false classification
  else:
    w_false = W[y_prime]
    w_correct = W[y]
    for i in range(len(x_vector)):
      w_false[i] -= x_vector[i]
      w_correct[i] += x_vector[i]
    # update the bias
    w_false[-1] -= 1
    w_correct[-1] += 1

    # put these weight vectors back into W
    W[y_prime] = w_false
    W[y] = w_correct
    return (W, True)  # No, there was no change to the weights

WEIGHTS = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
ALPHA = 1.0

def train_for_an_epoch(training_data, reporting=True):
  '''Go through the given training examples once, in the order supplied,
  passing each one to train_with_one_example.
  Return the weight vector and the number of weight updates.
  (If zero, then training has converged.)
  '''
  global WEIGHTS, ALPHA
  changed_count = 0
  # ADD YOUR CODE HERE
  for data in training_data:
    x_vector = [data[i] for i in range(len(data) - 1)]
    y = data[-1]

    (WEIGHTS, isChanged) = train_with_one_example(WEIGHTS, x_vector, y, ALPHA)

    if isChanged:
      changed_count += 1

  return changed_count

# THIS MAY BE HELPFUL DURING DEVELOPMENT:
TEST_DATA = [
[20, 25, 1, 1, 0],
[-2, 7, 2, 1, 1],
[1, 10, 1, 2, 1],
[3, 2, 1, 1, 2],
[5, -2, 1, 1, 2] ]

def test():
  print("Starting test with 3 epochs.")
  for i in range(3):
    train_for_an_epoch(TEST_DATA)
  print("End of test.")
  print("WEIGHTS: ", WEIGHTS)

if __name__=='__main__':
  test()

