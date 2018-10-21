from airalert.geos5 import TrainingDataExtractor

tde_cyprus = TrainingDataExtractor(
    [35.156264987959965, 33.34350585937501],
    [
        [35.263954145928686, 38.001708984375],
        [30.0185295116281, 33.71704101562501],
        [29.6469349313916, 38.19396972656251]
    ])

data = tde_cyprus.get_training_data()

import pprint

pprint.pprint(data)

import numpy
a = numpy.asarray(data)
numpy.savetxt("cyprus_input.csv", a, delimiter=",", fmt="%s")
