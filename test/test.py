
import subprocess
import threading
from hackrfthread import SpectrumWorker

# out = None

# def processStart():
#     out = subprocess.Popen(['hackrf_sweep', '-f2300:2500', '-w', '1000000', '-B'],
#                     stdout=subprocess.PIPE)
#     #stdout,stderr = out.communicate() #this gets it in a tuple. perhaps you don't need this.



# x = threading.Thread(target=processStart)

# x.start()

# while True:
#     print('in while loop')
#     try:
#         buf = out.stdout.read(4)
#     except AttributeError as e:
#         print('error')
#     if buf:
#         print('read byte')
#     else:
#         break
    
# x.join()

x = SpectrumWorker()
x.start()
x.join()
