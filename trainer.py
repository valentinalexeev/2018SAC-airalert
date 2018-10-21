import numpy as np
import tflearn

# Load CSV file, indicate that the first column represents labels
from tflearn.data_utils import load_csv
data, labels = load_csv('cyprus_train_model.csv', target_column=0,
                        categorical_labels=True, n_classes=5)

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
# Start training (apply gradient descent algorithm)
model.fit(data, labels, n_epoch=10, batch_size=16, show_metric=True)

model.save("cyprus.tflearn")
