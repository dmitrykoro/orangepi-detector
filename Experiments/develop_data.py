import json

import numpy
import numpy as np

import matplotlib.pyplot as plt


def develop_data():
    array = np.array(json.load(open('distances.json')))
    average = np.average(array)
    median = numpy.median(array)

    #plt.hist(array, bins='auto')
    #plt.show()

    plt.boxplot(array, vert=False, sym='.')
    plt.show()


    a = 5


develop_data()