import subprocess
import threading

# out = subprocess.Popen(['hackrf_sweep', '-1', '-r', 'test.csv'],
#                         stdout=subprocess.PIPE)
#stdout,stderr = out.communicate() #this gets it in a tuple. perhaps you don't need this.

class mythread(threading.Thread):


    def __init__(self):
        threading.Thread.__init__(self)
        self.process = None
        self.testvar = 1
        self.process = subprocess.Popen(['hackrf_sweep', '-1'],
                                stdout=subprocess.PIPE)

    def run(self):
        print('RUNNING PROCESS')
        while True:
            # print('Total number of threads', threading.activeCount())
            buf = thread1.process.stdout.read(4)
            if buf:
                print('read a byte')
            elif buf == '':
                print('no buffer')
                break
            else:
                print('break')
                break


thread1 = mythread()
thread1.start()

print('before while loop')
print('finished')
    

"""
#!/usr/bin/python
import subprocess, sys
## command to run - tcp only ##
cmd = "/usr/sbin/netstat -p tcp -f inet"
 
## run it ##
p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
 
## But do not wait till netstat finish, start displaying output immediately ##
while True:
    out = p.stderr.read(1)
    if out == '' and p.poll() != None:
        break
    if out != '':
        sys.stdout.write(out)
        sys.stdout.flush()

"""