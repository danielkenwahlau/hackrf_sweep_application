import math
import os
import struct
import subprocess
import threading
import time
import numpy as np  
import pdb
from sys import builtin_module_names
import gammarf_util
from gammarf_base import GrfModuleBase

HRF_FREQ_BYTES = 8
HRF_PWR_BYTES = 4
MOD_NAME = "spectrum"

"""
This class starts and runs the spectrum scan. It then populates a frequency map which is a list of the powers
at frequencies extracted from the hackrf_sweep.
"""

class SpectrumWorker(threading.Thread):
    def __init__(self):
        self.stoprequest = threading.Event()
        threading.Thread.__init__(self)

        self.freqmap = None
        self.freqmap_ready = False
        self.daemon = True

        #have to figure out this value
        self.step = None
        # self.step = 5000000


        #hardcoded values
        self.maxfreq = 2500000000
        self.minfreq = 2300000000


        # pdb.set_trace()
        ON_POSIX = 'posix' in builtin_module_names
        self.cmdpipe = subprocess.Popen([
            'hackrf_sweep',
            '-f2300:2500',
            '-w',
            '1000000',
            '-B'],
            stdout=subprocess.PIPE,
            stderr=open(os.devnull, 'w'),
            close_fds=ON_POSIX)

    def run(self):
        print('in run section')
        firstfreq = None
        total_freqs = 0
        while True:
            try:
                reclen, start, end = struct.unpack('=iqq',
                        self.cmdpipe.stdout.read(20))
            except:
                raise Exception("Problem communicating with HACKRF - exit and restart")

            if not firstfreq:
                firstfreq = start
            else:
                if start == firstfreq:
                    break

            pwr_entries = int((reclen - (HRF_FREQ_BYTES * 2))
                    / HRF_PWR_BYTES)

            if not self.step:
                self.step = int((end - start) / pwr_entries)
                # self.devmod.set_hackrf_step(self.step)

            try:
                self.cmdpipe.stdout.read(HRF_PWR_BYTES * pwr_entries)
            except:
                raise Exception("Problem communicating with HACKRF - exit and restart")

            total_freqs += pwr_entries
        
        self.freqmap = np.empty(total_freqs)
        while not self.stoprequest.isSet():
            
            try:
                pwrs = self.cmdpipe.stdout.read(HRF_PWR_BYTES * pwr_entries)
            except:
                raise Exception("Problem communicating with HACKRF - exit and restart")

            unpacked = list(struct.unpack('{}f'.format(pwr_entries), pwrs))

            substart = int((start - firstfreq)/self.step)
            substop = substart + pwr_entries

            self.freqmap[substart:substop] = list(unpacked)

            try:
                reclen, start, end = struct.unpack('=iqq',
                        self.cmdpipe.stdout.read(20))
            except:
                raise Exception("Problem communicating with HACKRF - exit and restart")

            if start == firstfreq:
                if not self.freqmap_ready:
                    self.freqmap_ready = True

        return    

    def is_freqmap_ready(self):
        return self.freqmap_ready

    def freqbin(self, freq):
        return math.floor((freq - self.minfreq) / self.step)

    def pwr(self, freq):
        if freq > self.maxfreq or freq < self.minfreq:
            return

        freqbin = int(self.freqbin(freq))
        return self.freqmap[freqbin]
    
    def freqrange(self,freq):
        bottomfreq = self.minfreq + (self.step * self.freqbin(freq))
        topfreq = bottomfreq + self.step
        return (bottomfreq, topfreq)

    def join(self, timeout=None):
        self.stoprequest.set()
        super(SpectrumWorker, self).join(timeout)
