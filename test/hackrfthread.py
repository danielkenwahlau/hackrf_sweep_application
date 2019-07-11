import math
import os
import struct
import subprocess
import threading
import time
import numpy as np  
from sys import builtin_module_names
import gammarf_util
from gammarf_base import GrfModuleBase

HRF_FREQ_BYTES = 8
HRF_PWR_BYTES = 4
MOD_NAME = "spectrum"

# def start():
#     return GrfModuleSpectrum()



class SpectrumWorker(threading.Thread):
    def __init__(self):
        self.stoprequest = threading.Event()
        threading.Thread.__init__(self)

        self.freqmap = None
        self.freqmap_ready = False
        self.daemon = True
        self.step = None

        ON_POSIX = 'posix' in builtin_module_names
        print('start command init')
        self.cmdpipe = subprocess.Popen([
            'hackrf_sweep',
            '-f2300:2500',
            '-w',
            '5000000',
            '-B'],
            stdout=subprocess.PIPE,
            stderr=open(os.devnull, 'w'),
            close_fds=ON_POSIX)
        print('finished init command')

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

        print('TOTALFREQS: ', total_freqs)
        self.freqmap = np.empty(total_freqs)
        while not self.stoprequest.isSet():
            try:
                pwrs = self.cmdpipe.stdout.read(HRF_PWR_BYTES * pwr_entries)
            except:
                raise Exception("Problem communicating with HACKRF - exit and restart")

            unpacked = list(struct.unpack('{}f'.format(pwr_entries), pwrs))

            substart = int((start - firstfreq)/self.step)
            substop = substart + pwr_entries

            print('unpack: ', list(unpacked))
            print('substart: ', substart)
            print('substop: ', substop)
            self.freqmap[substart:substop] = list(unpacked)

            print(self.freqmap)

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

        freqbin = self.freqbin(freq)
        return self.freqmap[freqbin]

    def join(self, timeout=None):
        self.stoprequest.set()
        super(SpectrumWorker, self).join(timeout)


# class GrfModuleSpectrum(GrfModuleBase):
#     def __init__(self):

#         self.description = "spectrum module"
#         self.settings = {}

#         self.worker = SpectrumWorker()
#         self.worker.daemon = True
#         self.worker.start()

#         self.thread_timeout = 3

#         gammarf_util.console_message("loaded", MOD_NAME)

#     def is_freqmap_ready(self):
#         """Check if the freqmap has been populated"""
#         return self.worker.is_freqmap_ready()

#     def freqbin(self, freq):
#         """Return bin in freqmap placed closest to input frequency"""
#         return self.worker.freqbin(freq)

#     def pwr(self, freq):
#         """Get power at a frequency according to the freqmap"""
#         return self.worker.pwr(freq)

# overridden 
