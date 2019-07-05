from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html');

import tflearn
import pprint

@app.route('/predict')
def predict():
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

    result = model.predict([[7,36, 10, 0, 30, 7, 25, 35, 1]])

    by_category = [
        {'0-50': result[0][0]},
        {'51-100': result[0][1]},
        {'101-150': result[0][2]},
        {'150-200': result[0][3]},
        {'201+': result[0][4]}
    ]
    return render_template('predict.html', {'by_category': by_category})
