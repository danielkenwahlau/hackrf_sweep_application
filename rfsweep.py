import csv
import string
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import argparse
from Qt import QtCore

#parse arguements
parser = argparse.ArgumentParser(description='Plots Hackrf Sweep Singleshot')
parser.add_argument('bin', type=int, nargs=1, help='the number of bins used for the sweep')
args = parser.parse_args()

print(args.bin[0])


sweepcsv = open('sweep.csv')

sweepcsvReader = csv.reader(sweepcsv)

frequencyDict = {}

#frequencies

freqArray = []
freqArrayIntermediate = []
dBArray = []
dBArrayIntermediate = []
rowCounter = 0

#this is the offset used to insert the 3rd row in between the first and second because of the way sweep 
#interleaves its entries.
insertIDX = args.bin[0] 
columOffset = 0
#print each row

#need to put in some code that that reads the first 3 entries first. Then proceed onto reading 4 at a time.
#once you pass the fist section then move on to processing the latter sections which are grouped in 4
#brute force for now and will clean this up into a function

firstSectionCounter = 0

for row in sweepcsvReader:
    print(','.join(row))

    if rowCounter == 2:
        columOffset = insertIDX        
    else:
        columOffset = 0

    freqlow = float(row[2])
    freqHigh = float(row[3])
    freqBin = float(row[4])
    #put first freq bin entry in dict
    #check if the frequency is already preset in the dictionary
    if freqlow not in frequencyDict:
        #if not in the dict then 
        frequencyDict[freqlow] = float(row[6])
        freqArrayIntermediate.insert(len(freqArrayIntermediate) - columOffset, freqlow)
        dBArrayIntermediate.insert(len(dBArrayIntermediate)- columOffset, float(row[6]))
    #keep adding entries based on bin size
    i = freqlow + freqBin
    freqPowerIdx = 0
    while i < freqHigh:
        frequencyDict[i] = float(row[7 + freqPowerIdx])
        freqArrayIntermediate.insert(len(freqArrayIntermediate) - columOffset, i)
        dBArrayIntermediate.insert(len(dBArrayIntermediate)- columOffset, float(row[7 + freqPowerIdx]))
        i += freqBin
        freqPowerIdx += 1
    
    #increment or reset row counter and append the "fixed" rows to the final array, clear the placeholder array
    if rowCounter == 2:
        rowCounter = 0
    else:
        rowCounter += 1
    
    if firstSectionCounter == 2:
        break
    else:
        firstSectionCounter += 1


#latter section of the sweep where the readings are grouped into 4. reset variables
rowCounter = 0
columOffset = 0

for row in sweepcsvReader:
    print(','.join(row))

    if rowCounter == 3:
        columOffset = insertIDX        
    else:
        columOffset = 0

    freqlow = float(row[2])
    freqHigh = float(row[3])
    freqBin = float(row[4])
    #put first freq bin entry in dict
    #check if the frequency is already preset in the dictionary
    if freqlow not in frequencyDict:
        #if not in the dict then 
        frequencyDict[freqlow] = float(row[6])
        freqArrayIntermediate.insert(len(freqArrayIntermediate) - columOffset, freqlow)
        dBArrayIntermediate.insert(len(dBArrayIntermediate)- columOffset, float(row[6]))
    #keep adding entries based on bin size
    i = freqlow + freqBin
    freqPowerIdx = 0
    while i < freqHigh:
        frequencyDict[i] = float(row[7 + freqPowerIdx])
        freqArrayIntermediate.insert(len(freqArrayIntermediate) - columOffset, i)
        dBArrayIntermediate.insert(len(dBArrayIntermediate)- columOffset, float(row[7 + freqPowerIdx]))
        i += freqBin
        freqPowerIdx += 1
    
    #increment or reset row counter and append the "fixed" rows to the final array, clear the placeholder array
    if rowCounter == 3:
        rowCounter = 0
    else:
        rowCounter += 1

    


fig, ax = plt.subplots()
ax.plot(freqArrayIntermediate, dBArrayIntermediate)

ax.set(xlabel='frequency (hz)', ylabel='Power(dB)',
       title='About as simple as it gets, folks')
ax.grid()

fig.savefig("freq.png")
plt.show()

sweepcsv.close()

