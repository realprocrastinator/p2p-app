# actions.py handle all user requests, all messages are sent using TCP/IP protocol
# functions:                      
# 1. peer join                    peer                    
# 2. peer exit gracefully         peer            
# 3. peer exit abruptly           peer        
# 4. store file                   peer
# 5. retrieve file                peer    

from threading import Thread
from msgtype import *
from socket import *
from para import *
from peers import *


host = parameters()["HOST_ADDR"]
PORT_BASE = int(parameters()["PORT_BASE"])



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
            pass
        # peer departure

        # peer lost

        # store file 

        # request file

        # close the TCP socket, open next time when get called again



# a TCP server listening for incoming request
class TCPSer(Thread):
    def __init__(self,t_name):
        Thread.__init__(self,name = t_name)
        self.sock = socket(AF_INET,SOCK_STREAM)
        #for debugging
        try:
            self.myid = int(uargs()["PEER_ID"])
        except Exception:
            self.myid = 2
        self.sock.bind((host,PORT_BASE + self.myid))
        self.sock.listen(5)
    
    def run(self):
        while True:
            # accept the new incoming connection
            conn,addr = self.sock.accept()
            Actors(conn,addr).start()

# a TCP client for sending 
class InfoClient(Thread):
    def __init__(self, server_id, info_type,
        info_val, requester_id = None):
        Thread.__init__(self)
        # store the passed in values
        self.server_id = server_id
        self.info_type = info_type
        self.info_val = info_val
        if requester_id:
            self.requester_id = requester_id
        else:
            self.requester_id = uargs()["PEER_ID"]

        # setup the socket 
        self.sock = socket(AF_INET, SOCK_STREAM)

    def run(self):
        self.sock.connect((host, PORT_BASE+self.server_id))
        msg = message()
        msg.setHeader(self.info_type, self.requester_id)
        msg.body = int2byte(self.info_val)
        # send the message 
        self.sock.send(msg.segment)
        # some cases we need to wait response and do callback 
        if self.info_type in [signal(header.PEER_LOST), signal(header.PEER_EXIT)]:
            msg = message(self.sock.recv(1024))
            if msg.header[0] == signal(header.PEER_EXIT_ACK):
                # exit granted
                # callback the controller 
                uargs()["options"].handle_peer_quit()
            elif msg.header[0] == signal(header.NEW_PEER):
                # register new peer
                uargs()["options"].hanlde_new_sus(
                    byte2int(msg.body)
                )

        # close the connection
        self.sock.close()