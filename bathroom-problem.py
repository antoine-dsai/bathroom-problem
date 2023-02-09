import logging
import random
import threading
import time
# print format
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-2s) %(message)s',
                    )

class ActivePool(object):
    def __init__(self):
        super(ActivePool, self).__init__()
        self.active = []
        self.lock = threading.Lock()
    
    def makeActive(self, name): #locks the door
        with self.lock:
            self.active.append(name)
            logging.debug('Enters Bathroom: %s', self.active)
    def makeInactive(self, name): #unlocks the door
        with self.lock:
            self.active.remove(name)
            logging.debug('Exits Bathroom: %s', self.active)


#creating process
def process(s, pool):
    with s:
        name = threading.currentThread().getName()
        pool.makeActive(name)                                                   #locks the door
        time.sleep(random.randint(3,11))                                        #random time spend in bathroom
        pool.makeInactive(name)                                                 #unlocks the door

pool = ActivePool()
s = threading.Semaphore(6)                                                      #creating smeaphores 

for i in range(100):
                                                                                #creating threads it gets argumants as student
    t = threading.Thread(target=process, name=str(i+1), args=(s, pool))
    t.start()