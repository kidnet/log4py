#(c) 2015, Jason Gao <goajian01735@pwrd.com>
#This file is part of Log4s Programe

from multiprocessing import Queue
from multiprocessing.managers import BaseManager
from log4s.exceptions import StatusError
import os
import time

#Message Queue.
MSQUEUE = Queue(-1)

#The class is a server of queue.
class QueueManager(BaseManager):
    pass

#Queue Server.
class Server(object):
    def __init__(self):
        #Create a message queue.
        self._timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
        self._qmanager = QueueManager()
        #Register 'get_queue' method.
        self._qmanager.register('get_queue', callable=lambda:MSQUEUE)
        self._server = None
        self._is_running = False
        self._port = False
        self._address = False
        self._socket = '/tmp/log4s.sock'

    #Listener a port on the address.
    def listener(self, address='', port=0, key='pwrd'):
        self._server = QueueManager(address=(address, port), authkey=key)

    #Start the queue server.
    def start(self, address='', port=0, key='pwrd'):
        if not self._server:
            self.listener(address, port, key)

        self._server.start()
        self._address, self._port = self._server.address
        self._is_running = True

    #Stop the queue server.
    def stop(self):
        if self._server and self._is_running:
            self._server.shutdown()
        else:
            raise StatusError("Server is not run.")
    
    #Create a socket file and input port.
    def _create_socket(self):
        path = os.path.basename(self._socket)
        if not os.path.exists(path):
            os.makedirs(path)
        elif os.path.exists(self._socket) and \
            not os.path.isfile(self._socket):
            backup_dir = self._socket + self._timestamp
            os.rename(self._socket, backup_dir)
        fhd = open(self._socket, 'wb')
        fhd.write(self._socket)
        fhd.close()
