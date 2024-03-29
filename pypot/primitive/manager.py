import threading
import numpy
import time

from collections import defaultdict
from functools import partial

class PrimitiveManager(threading.Thread):
    """ Combines all :class:`~pypot.primitive.primitive.Primitive` orders and affect them to the real motors. 
        
        At a predefined frequency, the manager gathers all the orders sent by the primitive to the "fake" motors, combined them thanks to the filter function and affect them to the "real" motors.
        
        .. note:: The primitives are automatically added (resp. removed) to the manager when they are started (resp. stopped).
        
        """
    def __init__(self, motors, freq=50, filter=partial(numpy.mean, axis=0)):
        """ :param motors: list of real motors used by the attached primitives
            :type motors: list of :class:`~pypot.dynamixel.motor.DxlMotor` 
            
            :param int freq: update frequency
            :param func filter: function used to combine the different request (default mean)
            
            """
        threading.Thread.__init__(self, name='Primitive Manager')
        self.daemon = True
        
        self._prim = []
        self._period = 1.0 / freq
        self._motors = motors
        self._filter = filter
        self._running = threading.Event()
        self._running.set()

    def add(self, p):
        """ Add a primitive to the manager. The primitive automatically attached itself when started. """        
        self._prim.append(p)

    def remove(self, p):
        """ Remove a primitive from the manager. The primitive automatically remove itself when stopped. """
        self._prim.remove(p)
    
    @property
    def primitives(self):
        """ List of all attached :class:`~pypot.primitive.primitive.Primitive`. """
        return self._prim

    def run(self):
        """ Combined at a predefined frequency the request orders and affect them to the real motors.
            
            .. note:: Should not be called directly but launch through the thread start method. 
            
            """
        while self._running.is_set():
            start = time.time()
            
            for m in self._motors:
                to_set = defaultdict(list)

                for p in self._prim:
                    for key, val in getattr(p.robot, m.name)._to_set.iteritems():
                        to_set[key].append(val)
        
                for key, val in to_set.iteritems():
                    filtred_val = self._filter(val)
                    setattr(m, key, filtred_val)
            
            end = time.time()
            
            dt = self._period - (end - start)
            if dt > 0:
                time.sleep(dt)

    def stop(self):
        """ Stop the primitive manager. """
        self._running.clear()