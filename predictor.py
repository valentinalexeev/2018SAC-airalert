"""
AirAlert predictor
----

Given 3 days of prior data attempt to predict 4th day using the trained model.
"""
import tflearn

# Build neural network
# 9 inputs (3 areas for 3 previous days)
net = tflearn.input_data(shape=[None, 9])
net = tflearn.fully_connected(net, 32)
net = tflearn.fully_connected(net, 32)
# 5 possible outputs
net = tflearn.fully_connected(net, 5, activation='softmax')
net = tflearn.regression(net)

# Define model
model = tflearn.DNN(net, tensorboard_verbose=3)
model.load("cyprus.tflearn")

print model.predict([[7,36, 10, 0, 30, 7, 25, 35, 1]])
