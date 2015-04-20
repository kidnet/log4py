#(c) 2015, Jason Gao <goajian01735@pwrd.com>
#This file is part of Log4s Programe

from multiprocessing import Queue
from multiprocessing.managers import BaseManager
from multiprocessing.managers import dispatch, listener_client, State
from log4s.exceptions import StatusError, ArgumentError
import os
import time

#Message Queue.
MSQUEUE = Queue(-1)

#The class is a server of queue.
class QueueManager(BaseManager):
    def connect(self):
        '''
        Connect manager object to the server process
        '''
        Listener, Client = listener_client[self._serializer]
        self._conn = Client(self._address, authkey=self._authkey)
        dispatch(self._conn, None, 'dummy')
        self._state.value = State.STARTED

    def close(self):
        self._conn.close()


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
        self._port = None
        self._address = None
        self._socket = '/tmp/log4s.sock'
        self.address = None

    #Listener a port on the address.
    def listener(self, address='', port=0, key='pwrd'):
        self._server = QueueManager(address=(address, port), authkey=key)

    #Start the queue server.
    def start(self, address='', port=0, key='pwrd'):
        if not self._server:
            self.listener(address, port, key)

        self._server.start()
        self.address = self._server.address
        self._address, self._port = self.address
        self._is_running = True
        if self._port:
            self._create_socket()

    #Stop the queue server.
    def stop(self):
        if self._server and self._is_running:
            self._server.shutdown()
        else:
            raise StatusError("Server is not run.")
    
    #Create a socket file and input port.
    def _create_socket(self):
        path = os.path.dirname(self._socket)
        if not os.path.exists(path):
            os.makedirs(path)
        elif os.path.exists(self._socket) and \
            not os.path.isfile(self._socket):
            backup_dir = self._socket + self._timestamp
            os.rename(self._socket, backup_dir)
        fhd = open(self._socket, 'wb')
        fhd.write(str(self._port))
        fhd.close()

class Clinet(object):
    def __init__(self):
        self._msqueue = Queue(-1)
        self._qmanager = QueueManager()
        self._qmanager.register('get_queue', callable=lambda:self._msqueue)
        self._socket = '/tmp/log4s.sock'
        self._address = ''
        self._port = None
        self._conn_status = False

    def _get_socket(self):
        if os.path.isfile(self._socket):
            fd = open(self._socket, 'rb')
            self._port = int(fd.readline())

    def connect(self, address='', port=None, key='pwrd'):
        if port:
            self._port = port
        else:
            self._get_socket()

        if self._port:
            self._client = self._qmanager(address=(address, self._port), authkey=key)
            self._conn_status = True
        else:
            err = "Port can\'t be \'None\'. Must provid a port number or \
                    start a server at localhost."
            raise ArgumentError(err)

    def get_queue(self):
        if self._conn_status:
            return self._client.get_queue()
        else:
            raise StatusError('Don\'t connect to server.')

#    def get(self):
#        if not self._remote_queue:
#            self._get_queue()
#        
#        return self._remote_queue.get()
#
#    def put(self, msg=None):
#        if not self._remote_queue:
#            self._get_queue()
#        
#        if msg:
#            self._remote_queue.put(msg)
#        else:
#            raise ArgumentError('Must provid a message to the queue.')

