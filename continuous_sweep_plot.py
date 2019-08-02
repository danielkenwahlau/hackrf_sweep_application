import time
import numpy as np
from scipy import signal
from modules.hackrfthread import SpectrumWorker
from modules.power_analysis_thread import PowerAnalysisWorker

#
SymaChArray = [2419500000,2435500000,2451500000,2467600000]

thread1 = SpectrumWorker(2400000000,2480000000,700000)
thread1.start()

#

freqRangeDict = {}
counter = 0
#about the number of sweeps that the hackrf can do with these parameters
sweepsPerSecond = 400
noiseThreshold = -58
transmissions = 3
droneDetected = False

#main
while True:

    time.sleep(.025)
    if thread1.is_freqmap_ready():
        for channel in SymaChArray:
            # print("freq range: {} hz power: {}".format(thread1.freqrange(channel),thread1.pwr(channel)))
            freqPwr = thread1.pwr(channel)
            freqRange = thread1.freqrange(channel)
            #Here if the power is greater -50 dB increment the number of instances else pass
            if freqRange not in freqRangeDict: #if the freqRange is not already in then set it to 0
                freqRangeDict[freqRange] = 0
            elif freqPwr > noiseThreshold:
                freqRangeDict[freqRange] += 1

            if counter >= sweepsPerSecond:
                # print freqRangeDict
                for value in freqRangeDict.values():
                    if value >= transmissions:
                        droneDetected = True
                    else:
                        droneDetected = False
                        break
                if droneDetected:
                    print freqRangeDict.values(), "Detect"
                else:
                    print(freqRangeDict.values())

                #sum up the number of activations in the dictionary or in each channel
                #if they are all greater than a certain amount of activations then we can say it's a drone of this class
                #clear the dictionary for the next pass
                freqRangeDict.clear()
                counter = 0
            else:
                counter += 1
    else:
        # print("freq not ready")
        continue



#sandbox
# while True:

#     time.sleep(.03)
#     if thread1.is_freqmap_ready():
#         for channel in SymaChArray:
#             # print("freq range: {} hz power: {}".format(thread1.freqrange(channel),thread1.pwr(channel)))
#             freqPwr = thread1.pwr(channel)
#             freqRange = thread1.freqrange(channel)

#             freqRangeDict[freqRange] = freqPwr
        
#         print freqRangeDict.values()

#     else:
#         # print("freq not ready")
#         continue