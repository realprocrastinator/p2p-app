"""
Jiawei Gao
z5242283
p2p network using DHT
"""
from threading import Thread, Timer, Lock
from para import parameters,uargs
from udpping import *
from peers import *
from actions import *
import os

port_base = parameters()["PORT_BASE"]


# interactive command handler
class InputHandler(Thread):
    def __init__(self):
        Thread.__init__(self)

    def isvalid(self,filename):
        try:
            result = (filename.isdigit() and \
                        len(filename)==4 and \
                        int(filename) <= 9999 and\
                        int(filename) >= 0)
            return result
        except Exception as e:
            return False
    
    # taking user input and use them to trigger event
    def run(self):

        commands = {"Request" : None,"Store" : None,"Quit" : None}

        while(True):
            argvs = input(">").split()
            if not argvs:
                # do nothing
                pass
            elif len(argvs) > 2:
                print("Invalid Command.")
                continue
            elif argvs[0].lower() == "quit":
                
                #TODO call Quit gracefully
                pass
            elif argvs[0].lower() == "request":
                if (len(argvs) != 2 or not self.isvalid(argvs[1])):
                    print("Invalid Command.")
                    continue
                else:
                    # TODO call commands[argv[0]](args[1])
                    pass
            elif argvs[0].lower() == "store":
                if (len(argvs) != 2 or not self.isvalid(argvs[1])):
                    print("Invalid Command.")
                else:
                    # TODO call commands[argv[0]](args[1])
                    pass
            else:
                print("Invalid Command.")
                continue
            

# handle different envents
class EventHandler(object):
    def __init__(self,id : int, peer_ids : list, no_ping = False):
        self.my_id = id
        
        # set up peer object
        self.peer = peer(self.my_id)
        self.myname = "peer_" + str(self.peer)

        # if we want to exit, we need to sync, use lock
        # we can only exit gracesully when no one is asking us for
        # info
        # TODO exit params  
        self.exit_approve = True
        self.big_lock = Lock()

        # parameters
        self.no_ping = no_ping
        self.peer_ids = peer_ids


    # p2pjoin()
    def p2pjoin(self):
        myid = self.my_id
        my_friend = uargs()["KNOWN_PEER"]
        # open TCP and send to my_friend, then wait for reply

        # if got reply then update the successors

        # call p2pinit() to start journey



    # p2pinit()
    def p2pinit(self):
        # TODO skip if noping flag is set for debugging
        if not self.no_ping:
            # add suc and ssuc to my peers 
            # init udp server
            # send ping info
            # if ping is successful is handled by ping
            self.print_ping_who(self.peer_ids)

            # TODO need to be synced!
            self.workers = []
            self.workers.append(self.add_suc("First",peer_ids[0]))
            self.workers.append(self.add_suc("Second",peer_ids[1]))           
            # TODO start the TCP receiver to handle the request

        
        # start udp ping server to receive the ping msg
        self.pingrcvr = pingReceiver(self.myname + "_pingrcvr")
        self.pingrcvr.start()

        # start to accept user input 
        InputHandler().start()


    # display sending msg
    def print_ping_who(self,suc: list):
        suc1, suc2 = suc[0],suc[1]
        print(f"Ping requests sent to Peers {suc1} and {suc2}")

    # function to send ping package and add successor
    def add_suc(self,order:str,peer_id:int):
        self.peer.add_suc(order,peer_id)
        # start the ping worker and send the ping to the successor
        worker = pingSender(self.myname + "pingSender",peer_id)
        worker.start()
        return worker

    # wrapping function to get the suc if no successor yet return NULL 
    def get_suc(self,order:str):
        suc = self.peer.get_suc(order)
        if not suc:
            print("I have no successor yet")
            return
        return suc

    # wrapping function to get the pre if no pre return NULL
    def get_pre(self,order:str):
        pre = self.peer.get_pre(order)
        if not pre:
            print("I have no predecessor yet")
            return
        return pre

    # display successors
    def print_successors(self):
        self.peer.print_successors

    # update the successors when join() get called 
    def suc_update(self,peer_id):
        self.suc_update(peer_id)
    
    # check if should join me
    def join_me(self,peer_id):
        return self.peer.join_me(peer_id)

    # handle_join()
    def handle_join(self,peer_id):
        # if peer will become my new suc then update get called
        # mean while disabling ping, after updating the peer.successors{}
        # then clean the enable ping
        if join_me(peer_id):
            # disable ping
            for worker in self.workers:
                worker.disable_ping()

            # TODO grab the lock!
            # update my successors table 
            self.suc_update(peer_id)
            
            # TODO tell my predecessor
            # wrap my_suc_id and send to pre to update his sec suc
            
            pass
        # otherwise  forward to my successor, tell him peer wants to join 
        else:
            # TODO tell my suc peer wants to join
            pass

    # peer is leaving the p2p network gracefully
    def peer_quit(self):
        # disable the ping
        for w in self.workers:
            w.disable_ping()
        
        # close the udp socket
        close(self.pingrcvr.sock)

        # TODO notice my predecessors 
        # tell them to update their successors

    # this function is thread safe
    def quit_allow(self):
        # If my peers allow me to leave then I can leave
        self.big_lock.acquire()
        self.exit_approve += 1
        if self.exit_approve == 2:
            # exit the thread
            print("Bye.")
            os._exit(0)
        self.big_lock.release()
    
        # TODO close TCP socket


    # when got the suc exit signal then call this function to handle
    # suc's departure
    def handle_peer_quit(self, quiter_id:int,order:str,new_suc:int):
        # display who is leaving
        print(f"Peer {quiter_id} will depart from the network")
        
        # help func, first suc or second suc? 
        def who(suc_id):
            sucs = self.peer.successor
            for k,v in sucs.items():
                if v == suc_id:
                    return k

        # remove the exiting suc
        self.peer.rem_suc(who(quiter_id))
        
        # disable ping such suc
        [w.disable_ping() for w in self.workers if w.suc_id == quiter_id]
        # update workers list
        self.workers = [w for w in self.workers if w.suc_id != quiter_id]

        # add a new worker for new suc
        self.handle_new_suc(order,new_suc)

        # display updating
        

    # add a new worker for ping new suc
    def handle_new_suc(self,order:str,new_suc:int):
        self.workers.append(self.add_suc(order,new_suc))
        self.print_successors()

    # 

def main():
    import sys

    if len(sys.argv) < 5:
        print("""Usage: p2p <init|join>   
                            <PEER> 
                            <FIRST_SUCCESSOR|KOWN_SUCCESSOR>
                            <SECOND_SUCCESSOR>
                            <PING_TINTERVAL>
                """)
        exit(1);

    # support multi windows 
    if sys.argv[0] == "python3":
        sys.argv.pop(0);

    uargs()["OPTIONS"] = sys.argv[1]
    uargs()["PEER_ID"] = sys.argv[2]
    
    if str(uargs()["OPTIONS"]).lower() == "init":
        
        if len(sys.argv) != 6:
            print("""Usage: p2p 
                            <TYPE> 
                            <PEER> 
                            <FIRST_SUCCESSOR> 
                            <SECOND_SUCCESSOR> 
                            <PING_TINTERVAL>
                """)
            exit(1);

        # TODO valid input check
        uargs()["FIRST_SUCCESSOR"] = int(sys.argv[3])
        uargs()["SECOND_SUCCESSOR"] = int(sys.argv[4])
        uargs()["PING_TINTERVAL"] = int(sys.argv[5])
        
        # TODO call p2pinit()
        uargs()["options"] = \
                    EventHandler(uargs()["PEER_ID"],
                                [uargs()["FIRST_SUCCESSOR"], uargs()["SECOND_SUCCESSOR"]],
                                )
        uargs()["options"].p2pinit()
        
    
    elif uargs()["OPTIONS"] == "join":

        if len(sys.argv) != 5:
            print("""Usage: p2p 
                            <TYPE> 
                            <PEER> 
                            <KNOWN_SUCCESSOR>  
                            <PING_TINTERVAL>
                """)
            exit(1);

        # TODO valid input check
        uargs()["KNOWN_PEER"] = int(sys.argv[3])    
        uargs()["PING_TINTERVAL"] = int(sys.argv[4])
        
        # TODO call p2pjoin() at this moment all p2pinit not called until such peer knows where to join!
        uargs()["options"] = EventHandler(uargs()["PEER_ID"],[])
        uargs()["options"].p2pjoin()
    
    else:
        print("Unkonwn Command. Usage: prog <init|join> <args>")
        exit(1)



if __name__ == "__main__":
    print("HI")
    main()

