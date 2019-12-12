
"""
12/12/2019 Matt Kennedy
This data set is a big larger than expected, but we don't actually need a very large sample to solve what we need
to solve. So lets just pick a few aircraft and iterate through the entire data set to extract the packets associated
with that aircraft. Further analysis can be done on just these aircraft datasets.
"""



# all imports here:
from glob import glob
import json
import numpy as np
import pandas as pd

from Code.final.JSONParsing import combineToICAODict, mergePackets



dataDir = '/media/matt/ext4-1/ADSB/2016-07-01/'
outputDir = '/media/matt/ext4-1/ADSB/processedData/'
allFiles = glob(dataDir + '*')


# select an aircraft that is flying in the middle of the day so we have the best chance of getting a lot of data
icaoDict = combineToICAODict( allFiles[600] )

allAircraftDFs, allMetaData = mergePackets(icaoDict)

largestDFs = np.argsort([df.shape[0] for df in allAircraftDFs])[::-1]

sampleSize = 25
wantedICAOs = [allAircraftDFs[n].ICAO[0] for n in largestDFs[:sampleSize]] # get the ICAO for the top sampleSize


# alright so now we want to iterate through the entire dataset and pull out any packets for these aircraft
wantedData = []
wantedMetaData = []
for n, path in enumerate(allFiles):

    print('Processing JSON', n, '/', len(allFiles))

    icaoDict = combineToICAODict( path )

    # just take the subset of ICAOs we actually want
    icaoDictSubset = {}
    for icao in wantedICAOs:
        if icao in icaoDict:
            icaoDictSubset[icao] = icaoDict[icao]
    if len(icaoDictSubset) == 0:
        continue

    allAircraftDFs, allMetaData = mergePackets(icaoDictSubset)

    wantedData += allAircraftDFs
    wantedMetaData.append( allMetaData )


# merge them all into a single DF?
wantedDataDF = pd.concat(wantedData)
wantedMetaDataDF = pd.concat(wantedMetaData)

wantedDataDF = wantedDataDF.sort_values(by=['ICAO','PosTime'])  # and sort by the timestamps

wantedDataDF.to_csv(outputDir+'dataSubset.csv', index=False)
wantedMetaDataDF.to_csv(outputDir+'metaDataSubset.csv', index=False)




