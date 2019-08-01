import time
import numpy as np
from scipy import signal
from modules.hackrfthread import SpectrumWorker
from modules.power_analysis_thread import PowerAnalysisWorker

#
SymaChArray = [2420000000,2435000000,2451000000,2467000000]

thread1 = SpectrumWorker(2300000000,2500000000,300000)
thread1.start()

#

freqRangeDict = {}
counter = 0
#about the number of sweeps that the hackrf can do with these parameters
sweepsPerSecond = 40 


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
            elif freqPwr > -60:
                freqRangeDict[freqRange] += 1

            if counter >= sweepsPerSecond:
                print freqRangeDict
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