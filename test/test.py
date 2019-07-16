import subprocess
import threading
import time
import sys
from hackrfthread import SpectrumWorker

thread1 = SpectrumWorker()
thread1.start()

# testing freqmap
# freqmap[190:195] = [1,2,3,4,5]

# print(freqmap)