
# this is a docstring that describes what the file does
"""
12/10/2019 Matt Kennedy
First step of the data exploration process - what libraries/methods should we be using to read in the JSON files?
"""



# all imports here:
from glob import glob
import json


# and then start the code
dataDir = '/media/matt/ext4-1/ADSB/2016-07-01/'
allFiles = glob(dataDir + '*')

# lets first try the standard json package
with open(allFiles[800], 'r') as f:
    fileData = json.load(f)

# alright so seems this works great and does exactly what we need
# this loads in the file as a dictionary, where the data is contained in the top level key 'acList'
# 'acList' seems to be a list of dictionaries, where each item is a packet received from an aircraft

# lets reformat this into a new dictionary where the keys are the aircraft ICAO

# I have some fancier data structures in the Python shared libraries at work to do easily do operations like this,
# but for now lets just use pure Python
icaoDict = {}
for packet in fileData['acList']: # iterate through the list of packets
    # packet is a dictionary
    icao = packet['Id'] # icao is the aircraft identifier

    # add this packet to the aircraft's packet list
    if icao not in icaoDict:
        icaoDict[icao] = [packet] # initialize a new list for this aircraft
    else:
        icaoDict[icao].append( packet ) # else add it to the existing one

# and lets just walk through the debugger and confirm that the above is working as expected
# and maybe print out some results:
print('Found', len(icaoDict), 'aircraft in this time stamp')

print('The top 10 aircraft with most packets are:')
numPackets = sorted([(len(icaoDict[icao]), icao) for icao in icaoDict])[::-1]
for (num, icao) in numPackets[0:10]:
    print(num, icao)

# huh... well it seems to be working, however there is only one time stamp per aircraft in this file
# that seems concerning, but not necessarily incorrect





