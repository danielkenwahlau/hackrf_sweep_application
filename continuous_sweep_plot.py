import time
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

from modules.hackrfthread import SpectrumWorker

thread1 = SpectrumWorker()

thread1.start()

while True:
    if thread1.freqmap_ready():
        
    continue

# print(thread1.freqmap)