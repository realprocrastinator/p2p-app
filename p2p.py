"""
Jiawei Gao
z5242283
p2p network using DHT
"""
from threading import Thread
from para import parameters,uargs
import os

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
    def __init__(self,id : int, peers : list, no_ping = False):
        self.my_id = id
        
        # TODO set up peer object
        
        # TODO skip if noping flag is set for debugging
        if not no_ping:
            # add suc and ssuc to my peers 
            # init udp server
            # send ping info
            # if ping is successful is handled by ping
            pass
    
    #start to accept user input 
    InputHandler().run()

    # if we want to exit, we need to sync, use lock
    # we can only exit gracesully when no one is asking us for
    # info
    # TODO exit params  


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
        
        pass
    
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
        
        # TODO call p2pjoin()
        pass
    
    else:
        print("Unkonwn Command. Usage: prog <init|join> <args>")
        exit(1)



if __name__ == "__main__":
    print("HI")
    main()

