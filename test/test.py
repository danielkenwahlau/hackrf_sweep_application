import subprocess
import threading

class mythread(threading.Thread):
    def __init__(self, i):
        threading.Thread.__init__(self)
        self.h = i

    def run(self):
        print('Value send', self.h)

thread1 = mythread(1)
thread1.start()