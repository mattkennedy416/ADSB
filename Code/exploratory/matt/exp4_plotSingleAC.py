

"""
12/12/2019 Matt Kennedy
So now that we extracted a subset of the data, lets plot it up and see what it looks like.
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

dataDir = '/media/matt/ext4-1/ADSB/processedData/'

data = pd.read_csv(dataDir+'dataSubset.csv')


for icao in np.unique(data.ICAO.values):

    dataSubset = data[data.ICAO == icao]

    plt.plot(dataSubset['Lat'], dataSubset['Long'], '.')
    plt.title(icao)

    plt.show()


