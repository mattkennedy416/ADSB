
"""
12/10/2019 Matt Kennedy
So in the previous file we tested the JSON reader and created a new dictionary with the keys being the icao codes.
We only found one time stamp per minute for each aircraft, but lets see how things look when we start combining
data from multiple files.
"""


# all imports here:
from glob import glob
import json
import numpy as np
import pandas as pd
import pickle


# functions should go after imports, with any code not in a function at the very bottom
# lets first create a function from the work done in the previous file
def combineToICAODict(filepath, icaoDict):
    # Create a docstring for each function. If you fully define the function first (with inputs) then it should
    # auto-populate the param fields below. Fill them out describing each parameter!
    # seems trivial here, but still a good habit and can be critical for more complicated things
    """
    This function takes in a filepath to a single ADSB Timestamp JSON file and converts them to an ICAO based dictionary
    :param filepath: filepath to ADSB JSON file
    :param icaoDict: master icao dict - lets try just passing the same object back and forth to ease the merging
    :return: dictionary of aircraft packets
    """

    # just copying the same methodology as before:
    with open(filepath, 'r') as f:
        fileData = json.load(f)

    # icaoDict = {}
    for packet in fileData['acList']:
        icao = packet['Icao']

        # add this packet to the aircraft's packet list
        if icao not in icaoDict:
            icaoDict[icao] = [packet]  # initialize a new list for this aircraft
        else:
            icaoDict[icao].append(packet)  # else add it to the existing one

    return icaoDict





# and then start the code
dataDir = '/media/matt/ext4-1/ADSB/2016-07-01/'
outputDir = '/media/matt/ext4-1/ADSB/processedData/'
allFiles = glob(dataDir + '*')

# lets first test a few:
icaoDict = {} # master icao dictionary
for n, filepath in enumerate(allFiles[615:620]):
    print('Processing JSON', n, '/', len(allFiles))
    icaoDict = combineToICAODict( filepath, icaoDict )


# lets again check the statistics on these:
print('Found', len(icaoDict), 'aircraft in this time stamp')

print('The top 10 aircraft with most packets are:')
numPackets = sorted([(len(icaoDict[icao]), icao) for icao in icaoDict])[::-1]
for (num, icao) in numPackets[0:10]:
    print(num, icao)


# alright this looks reasonable now
# so within each of these packets the data that we actually want is in the "Cos" entry, which from the docs is:
# "Short Trails (Cos) are a list of values that represent the positions that the aircraft has been seen
# in over so-many seconds (by default 30 seconds)."

# this parameter actually a 4 column array that's been flattened to a list, where the columns are:
# - lat (degrees)
# - long (degrees)
# - timestamp (PosTime = unix time in milliseconds)
# - altitude (feet)

# would like to create a 4 column Pandas DataFrame for each aircraft timeseries data
# in addition to a row entry into a global descriptor of aircraft meta-data

allAircraftDFs = []
allMetaDataDFs = []

for n, icao in enumerate(icaoDict):

    print('Processing aircraft', n, '/', len(icaoDict))

    aircraftDFs = [] # keep a list of dataframes from each packet, and we'll concatenate them together at the end

    for packet in icaoDict[icao]:
        if 'Cos' in packet: # not sure it's guaranteed to be
            shortTrail = np.array(packet['Cos']).reshape( -1, 4 ) # unflatten it to an Nx4 array
            df = pd.DataFrame(columns=['Lat','Long','PosTime','Alt'], data=shortTrail) # turn this into a dataframe

            aircraftDFs.append(df) # and append

    if len(aircraftDFs) > 0:
        timeseriesDF = pd.concat(aircraftDFs) # merges a list of dataframes into a single dataframe
        timeseriesDF = timeseriesDF.sort_values(by='PosTime') # and sort by the timestamps

        if timeseriesDF.shape[0] < 5:
            continue # not enough data for us to care about

        # outputFilename = str(icao)+'.csv'
        # timeseriesDF.to_csv(outputDir+outputFilename, index=False)

        # saving many individual small files is typically a bad idea, as well as having many small pandas dataframes
        # lets store them all in a single dataframe with the icao as the key?
        # so need to add an extra column
        keyCol = timeseriesDF.shape[0] * [icao]
        timeseriesDF['ICAO'] = keyCol
        allAircraftDFs.append(timeseriesDF)

        # we also want to track the meta-data
        # should theoretically be the same from all packets ... so lets just take info from the first packet?
        # I guess rather than specify which columns we do want, lets just specify which we don't
        unwantedCols = ['Alt','AltT','Bad','Cos','GAlt','Gnd', 'InHg','Lat','Long'] # might have a few extra in there that are useless, but we don't really care
        wantedCols = [col for col in icaoDict[icao][0] if col not in unwantedCols]

        metaDataRowValues = [icaoDict[icao][0][col] for col in wantedCols]

        # sometimes some of these elements come out as a list? like the airport name? lets just merge
        for n, val in enumerate(metaDataRowValues):
            if isinstance(val, list):
                metaDataRowValues[n] = ' '.join(val)

        metaDataRowValues = np.array(metaDataRowValues).reshape(1,-1) # needs to be a 1xN array for pandas to accept it
        metaDataRowDF = pd.DataFrame(columns=wantedCols, data=metaDataRowValues)

        allMetaDataDFs.append( metaDataRowDF )


allMetaData = pd.concat(allMetaDataDFs)
allMetaData.to_csv(outputDir+'MetaData.csv',index=False) # we can leave this as a csv though

allAircraftData = pd.concat(allAircraftDFs)
allAircraftData.to_csv(outputDir+'allAircraftData.csv', index=False)

