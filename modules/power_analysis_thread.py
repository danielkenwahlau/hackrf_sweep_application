import threading
"""
This class runs after the frequency map has been formed and we can start to poll and do power analysis. 
It will return the proper drone class.
"""


class PowerAnalysisWorker(threading.Thread):
    def __init__(self,min,max,binWidth):
        threading.Thread.__init__(self)
        
    def run(self):
        return    