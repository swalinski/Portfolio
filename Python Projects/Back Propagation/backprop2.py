import numpy as np
import math
from tensorflow.examples.tutorials.mnist import input_data

# Neural network has four layers
# The input layer has 784 nodes
# The two hidden layers each have 5 nodes
# The output layer has 10 nodes
num_layer = 4
num_node = [784,5,5,10]
num_output_node = 10

# 30000 training sets are used
# 10000 test sets are used
# Can be adjusted
Ntrain = 30000
Ntest = 10000

# Sigmoid Function
def g(X):
    return 1/(1 + np.exp(-X))

# Forwardpropagation
def h(W,X):
    a = X
    for l in range(num_layer - 1):
        a = np.insert(a,0,1)
        z = np.dot(a,W[l])
        a = g(z)
    return a      

# Cost Function
def J(y, W, X, Lambda):
    cost = 0
    for i in range(Ntrain):
        H = h(W,X[i])
        for k in range(num_output_node):            
            cost = cost + y[i][k] * math.log(H[k]) + (1-y[i][k]) * math.log(1-H[k])
    regularization = 0
    for l in range(num_layer - 1):
        for i in range(num_node[l]):
            for j in range(num_node[l+1]):
                regularization = regularization + W[l][i+1][j] ** 2
    return (-1/Ntrain * cost + Lambda / (2*Ntrain) * regularization)

# Backpropagation - confirmed to be correct
# Algorithm based on https://www.coursera.org/learn/machine-learning/lecture/1z9WW/backpropagation-algorithm
# Returns D, the value of the gradient
def BackPropagation(y, W, X, Lambda):
    delta = np.empty(num_layer-1, dtype = object)
    for l in range(num_layer - 1):
        delta[l] = np.zeros((num_node[l]+1,num_node[l+1]))
    for i in range(Ntrain):
        A = np.empty(num_layer-1, dtype = object)
        a = X[i]
        for l in range(num_layer - 1):
            A[l] = a
            a = np.insert(a,0,1)
            z = np.dot(a,W[l])
            a = g(z)
        diff = a - y[i]
        delta[num_layer-2] = delta[num_layer-2] + np.outer(np.insert(A[num_layer-2],0,1),diff)
        for l in range(num_layer-2):
            index = num_layer-2-l
            diff = np.multiply(np.dot(np.array([W[index][k+1] for k in range(num_node[index])]), diff), np.multiply(A[index], 1-A[index])) 
            delta[index-1] = delta[index-1] + np.outer(np.insert(A[index-1],0,1),diff)
    D = np.empty(num_layer-1, dtype = object)
    for l in range(num_layer - 1):
        D[l] = np.zeros((num_node[l]+1,num_node[l+1]))
    for l in range(num_layer-1):
        for i in range(num_node[l]+1):
            if i == 0:
                for j in range(num_node[l+1]):
                    D[l][i][j] = 1/Ntrain * delta[l][i][j]
            else:
                for j in range(num_node[l+1]):
                    D[l][i][j] = 1/Ntrain * (delta[l][i][j] + Lambda * W[l][i][j])
    return D

# Neural network - this is where the learning/adjusting of weights occur
# W is the weights
# learn is the learning rate
# iterations is the number of iterations we pass over the training set
# Lambda is the regularization parameter
def NeuralNetwork(y, X, learn, iterations, Lambda):

    W = np.empty(num_layer-1, dtype = object)
    for l in range(num_layer - 1):
        W[l] = np.random.rand(num_node[l]+1,num_node[l+1])/100
    for k in range(iterations):
        print(J(y, W, X, Lambda))
        D = BackPropagation(y, W, X, Lambda)
        for l in range(num_layer-1):
            W[l] = W[l] - learn * D[l]
    print(J(y, W, X, Lambda))
    return W

mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

# Training data, read from MNIST
inputpix = []
output = []

for i in range(Ntrain):
    inputpix.append(2 * np.array(mnist.train.images[i]) - 1)
    output.append(np.array(mnist.train.labels[i]))

np.savetxt('input.txt', inputpix, delimiter=' ')
np.savetxt('output.txt', output, delimiter=' ')

# Train the weights
finalweights = NeuralNetwork(output, inputpix, 2, 5, 1)

# Test data
inputtestpix = []
outputtest = []

for i in range(Ntest):
    inputtestpix.append(2 * np.array(mnist.test.images[i]) - 1)
    outputtest.append(np.array(mnist.test.labels[i]))

np.savetxt('inputtest.txt', inputtestpix, delimiter=' ')
np.savetxt('outputtest.txt', outputtest, delimiter=' ')

# Determine the accuracy of the training data
count = 1  # 0
for i in range(Ntrain):
    H = h(finalweights,inputpix[i])
    #print(H)
    for j in range(num_output_node):
        if H[j] == np.amax(H) and output[i][j] == 1:
            count = count + 1
print(count/Ntrain)

# Determine the accuracy of the test data
count = 1    # 0
for i in range(Ntest):
    H = h(finalweights,inputtestpix[i])
    #print(H)
    for j in range(num_output_node):
        if H[j] == np.amax(H) and outputtest[i][j] == 1:
            count = count + 1
print(count/Ntest)
