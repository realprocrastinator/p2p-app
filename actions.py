# actions.py handle all user requests, all messages are sent using TCP/IP protocol
# functions:                      
# 1. peer join                    peer                    
# 2. peer exit gracefully         peer            
# 3. peer exit abruptly           peer        
# 4. store file                   peer
# 5. retrieve file                peer    

from threading import Thread
from msgtype import *
from socket import socket
from para import *
from peers import *

"""
rev from the other peers request, and handle the request 
"""
class Actors(Thread):
    def __init__(self,t_name:str,conn:socket, addr):
        Thread.__init__(self,name = t_name)
        self.conn = conn
        self.addr = addr
    def run(self):
        # get the msg from buffer
        msg = self.conn.recv(2048)
        # decode the msg
        action = message(msg).header[0]
        peer_id = message(msg).header[1]
        # accessing swicth table and handle the event
        
        # peer join
        if action == signal(header.PEER_JOIN):
            # call Eventhandler

        # peer departure

        # peer lost

        # store file 

        # request file

        # close the TCP socket, open next time when get called again

