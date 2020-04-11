from socket import *
from threading import Thread
from time import sleep
from para import *
from msgtype import *

host = parameters()["HOST_ADDR"]
try: 
    MYID = int(uargs()["PEER_ID"])
except Exception:
    # just for DEBUGGING
    MYID = -1
PORT_BASE = int(parameters()["PORT_BASE"])
port = PORT_BASE + MYID
try:
    PING_INTERVAL = int(uargs()["PING_INTERVAL"])
except Exception:
    PING_INTERVAL = 5
"""
a pingReceiver once received the package call
update() method to update the predecessor and can 
send the ping package along with ACK_PING headerand
its peer_id back to its predecessor
"""
class pingReceiver(Thread):
    def __init__(self,t_name:str):
        # give thread a name for easier debugging
        Thread.__init__(self,name=t_name)
        
        # create a UDP socket, using IPv4 addr
        self.sock = socket(AF_INET,SOCK_DGRAM)
        # bind the socket to a port
        self.sock.bind((host,port))
        self.segment = None

    def ack_Ping(self,msg: message, addr):
        # at this moment we received the msg from
        # our predecessor successfully so, we will
        # send the acknowledgment back
        
        # get the predecessor id from the msg and print out
        pre_id = msg.header[1]
        print(f"Ping request message received from Peer {str(pre_id)}")

        #TODO update the predecessor, call add predecessor

        # construct the ack msg
        ack_msg = message()
        ack_msg.setHeader(header.ACK_PING.value,MYID)

        self.sock.sendto(msg.segment,addr)
    
    def run(self):
        # waiting for the receiver buffer, once got the
        # msg from another peer then ack back
        while True:
            data,addr = self.sock.recvfrom(2048)

            # deconstruct the message
            msg = message(data)
            
            if msg.header[0] == header.SND_PING.value:
                self.ack_Ping(msg,addr)
            else:
                print("something wrong with the buffer. Sync prob?")

        # we never expect to go here
        print("I'm dead...I can't handle that...")
        exit(1)

"""
1. a pingSender can send ping package to its successor and second
successor, once sent it will always try to wait for reply

2. a pingSender can receive the ACK_PING signal sent by the 
successor if timeout occurs then reduce the live probability, 
if probability reaches threshold then a loss event occurs, 
it will call the update() method to update its successor
"""
class pingSender(Thread):
    def __init__(self,t_name:str,peer_id:int):
        Thread.__init__(self)
        
        # each timeout will reduce the rivival chance by 1, 
        # suc viewed as dead if reaches 0
        self.revival_chance = 3

        # create UDP socket and set timeout 
        self.sock = socket(AF_INET,SOCK_DGRAM)
        # pingReceiver always starts first and already bind the socket
        # so no need to bind again
        self.sock.settimeout(1)

        # send to who?
        self.peer_id = peer_id

    def sendPing(self,chance:int):
        if chance == 0:
            #TODO suc died, call update()
            print(f"peer{self.peer_id} is lost, updating successors...")
        else:
            # construct the message
            ping_msg = message()
            ping_msg.setHeader(header.SND_PING.value,PORT_BASE + self.peer_id)
            # send the ping
            self.sock.sendto(ping_msg.segment,(host,PORT_BASE+self.peer_id))
            try:
                # wait for reply, if timeout, reduce chance and try again
                ack_data, addr =  self.sock.recvfrom(2048)
                msg = message(ack_data)

                # the package should be an ack_ping package, otherwise something weird happend
                if msg.header[0] == header.ACK_PING.value:
                    suc_id = msg.header[1]
                    print(f"Ping response received from Peer {suc_id}")

                    # Since our successor is alive lets wait for a while
                    # and resend the ping
                    sleep(PING_INTERVAL) 
                else:
                    # not ping msg
                    print("Something wrong with the buffer!")
                    exit(1)
            except timeout:
                # reduce the chance by one and try again
                self.sendPing(chance - 1)

    # TODO add a stop method for debugging

    def run(self):
        # TODO is that enough?
        # actually the periodically sending ping request
        # can be done in a higher level
        self.sendPing(3)






if __name__ == "__main__":
    MYID = uargs()["PEER_ID"] = 2
    print(header.ACK_PING.value)
    print(MYID)
    pingReceiver("PingReceiver").start()
    MYID = 3
    pingSender("PingSender",-1).start()
    print("main thread finished...")
    while True:
        sleep(0.1)

