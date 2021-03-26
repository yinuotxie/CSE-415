'''binary_perceptron.py
One of the starter files for use in CSE 415, Winter 2021
Assignment 6.

Version of Feb. 18, 2021

'''

def student_name():
  return "Travis Xie" # Replace with your own name.

def classify(weights, x_vector):
  '''Assume weights = [w_0, w_1, ..., w_{n-1}, biasweight]
     Assume x_vector = [x_0, x_1, ..., x_{n-1}]
       Note that y (correct class) is not part of the x_vector.
     Return +1 if the current weights classify this as a Positive,
        or  -1 if it seems to be a Negative.
  '''
  # bias input should be always 1
  # the last element is the biasweight
  y = weights[-1] * 1
  for i in range(len(x_vector)):
    y += weights[i] * x_vector[i]
  
  if y > 0: return 1
  else: return -1


def train_with_one_example(weights, x_vector, y, alpha):
  '''Assume weights are as in the above function classify.
     Also, x_vector is as above.
     Here y should be +1 if x_vector represents a positive example,
      and -1 if it represents a negative example.
     Learning rate is specified by alpha.
  '''
  # Implement your code here.
  y_prime = classify(weights, x_vector)

  # misclassified
  if y_prime != y:
    if y == 1:  s = + 1
    
    if y == -1: s = -1

    for i in range(len(x_vector)):
      weights[i] += s * alpha * x_vector[i]

    weights[-1] += s * alpha * 1

    return (weights, True) # weights are changed
  else:
    return (weights, False)

# From here on use globals that can be easily imported into other modules.
WEIGHTS = [0,0,0]
ALPHA = 0.5

def train_for_an_epoch(training_data, reporting=True):
  '''Go through the given training examples once, in the order supplied,
  passing each one to train_with_one_example.
  Update the global WEIGHT vector and return the number of weight updates.
  (If zero, then training has converged.)
  '''
  global WEIGHTS, ALPHA
  changed_count = 0

  for data in training_data:
    x_vector = [data[i] for i in range(len(data) - 1)]
    y = data[-1]

    (WEIGHTS, isChanged) = train_with_one_example(WEIGHTS, x_vector, y, ALPHA)

    if isChanged:
      changed_count += 1

  return changed_count


TEST_DATA = [
[-2, 7, +1],
[1, 10, +1],
[3, 2, -1],
[5, -2, -1] ]

def test():
  print("Starting test with 3 epochs.")
  for i in range(3):
    train_for_an_epoch(TEST_DATA)
  print(WEIGHTS)
  print("End of test.")

if __name__=='__main__':
  test()

