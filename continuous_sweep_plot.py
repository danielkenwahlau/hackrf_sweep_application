import time
import numpy as np
from scipy import signal
from modules.hackrfthread import SpectrumWorker

SymaChArray = [2420000000,2435000000,2451000000,2467000000]

thread1 = SpectrumWorker()
thread1.start()

#main
while True:

    time.sleep(1)
    if thread1.is_freqmap_ready():
        for channel in SymaChArray:
            print("freq range: {} hz power: {}".format(thread1.freqrange(channel),thread1.pwr(channel)))
    else:
        print("freq not ready")
        continue

