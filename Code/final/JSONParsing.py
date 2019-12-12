

import json
import pandas as pd
import numpy as np


def combineToICAODict(filepath, icaoDict=None):
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

    if icaoDict is None:
        icaoDict = {}

    for packet in fileData['acList']:
        icao = packet['Icao']

        # add this packet to the aircraft's packet list
        if icao not in icaoDict:
            icaoDict[icao] = [packet]  # initialize a new list for this aircraft
        else:
            icaoDict[icao].append(packet)  # else add it to the existing one

    return icaoDict


def mergePackets(icaoDict):
    """
    Process an ICAO Dict to individual aircraft time series and meta-data
    :param icaoDict:
    :return:
    """
    allAircraftDFs = []
    allMetaDataDFs = []

    # I guess rather than specify which columns we do want, lets just specify which we don't
    unwantedCols = ['Alt', 'AltT', 'Bad', 'Cos', 'GAlt', 'Gnd', 'InHg', 'Lat',
                    'Long']  # might have a few extra in there that are useless, but we don't really care
    wantedCols = [col for col in icaoDict[list(icaoDict.keys())[0]][0] if col not in unwantedCols]
    metaDataRowValues = [icaoDict[list(icaoDict.keys())[0]][0][col] for col in wantedCols]

    for n, icao in enumerate(icaoDict):

        print('Processing aircraft', n, '/', len(icaoDict))

        aircraftDFs = []  # keep a list of dataframes from each packet, and we'll concatenate them together at the end

        for packet in icaoDict[icao]:
            if 'Cos' in packet:  # not sure it's guaranteed to be
                shortTrail = np.array(packet['Cos']).reshape(-1, 4)  # unflatten it to an Nx4 array
                df = pd.DataFrame(columns=['Lat', 'Long', 'PosTime', 'Alt'],
                                  data=shortTrail)  # turn this into a dataframe

                aircraftDFs.append(df)  # and append

        if len(aircraftDFs) > 0:
            timeseriesDF = pd.concat(aircraftDFs)  # merges a list of dataframes into a single dataframe
            timeseriesDF = timeseriesDF.sort_values(by='PosTime')  # and sort by the timestamps

            if timeseriesDF.shape[0] < 5:
                continue  # not enough data for us to care about

            # saving many individual small files is typically a bad idea, as well as having many small pandas dataframes
            # lets store them all in a single dataframe with the icao as the key?
            # so need to add an extra column
            keyCol = timeseriesDF.shape[0] * [icao]
            timeseriesDF['ICAO'] = keyCol
            allAircraftDFs.append(timeseriesDF)

            # we also want to track the meta-data
            # should theoretically be the same from all packets ... so lets just take info from the first packet?
            # sometimes some of these elements come out as a list? like the airport name? lets just merge
            for n, val in enumerate(metaDataRowValues):
                if isinstance(val, list):
                    metaDataRowValues[n] = ' '.join(val)

            metaDataRowValues = np.array(metaDataRowValues).reshape(1,-1)  # needs to be a 1xN array for pandas to accept it
            metaDataRowDF = pd.DataFrame(columns=wantedCols, data=metaDataRowValues)

            allMetaDataDFs.append(metaDataRowDF)

    if len(allMetaDataDFs) > 0:
        allMetaData = pd.concat(allMetaDataDFs)
    else:
        allMetaData = pd.DataFrame(columns=wantedCols)

    return allAircraftDFs, allMetaData

