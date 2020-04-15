
from threading import Lock
from para import *

class peer(object):
    def __init__(self,id : int):
        self.my_id = id
        self.predecessor = {}
        self.successor = {}
        # by receiving the ping msg
        # from my predecessor I can know who he is
        # but I need a lock to protect the shared predecessor list 
        self.peer_lock = Lock()

    # add suc
    def add_suc(self,order:str,id:int):
        self.successor[order] = id

    # add pres
    def add_pre(self,order:str,id:int):
        # critical region
        self.predecessor[order] = id

    # rem suc order is first or second
    def rem_suc(self,order:str):
        try:
            del self.successor[order]
        except KeyError:
            print("I dont have such successor.")

    # rem pre
    def rem_pre(self,order:str):
        self.pre_lock.acquire()
        try:
            del self.predecessor[order]
        except KeyError:
            print("I dont have such predecessor.")
        self.pre_lock.release()

    # get suc id
    def get_suc(self,order:str):
        if self.successor:
            return self.successor[order]
    
    # get pre id
    def get_pre(self,order:str):
        if self.predecessor:
            return self.predecessor[order]
    
    # get my id
    def get_myid(self):
        return self.my_id

    # update successors of me
    def suc_update(self,peer_id,flag = None):
        if not flag:
            # update the peer who has been joined
            self.successor["second"] =  self.successor["first"]
            self.successor["first"] = peer_id
        elif flag == signal(header.JOIN_UPDATE):
            # update the first predecessor's second suc
            self.successor["second"] = peer_id
        

    # 
    def print_successors(self):
        try:
            suc1,suc2 = self.successor["first"],self.successor["second"]
            print (f"My new first successor is Peer {str(suc1)}")
            print (f"My new Second successor is Peer {str(suc2)}")
        except Exception:
            pass
    # check if I should be responsible for such file
    # if yes then lookup my local file table
    def has_file(self,file_id):
        hash = file_id % 256
        if self.get_pre("first") <= self.get_myid():
            # I'm not the peer with the smallest id
            if hash > self.get_pre("first") and hash <= self.get_myid():
                return True
        else:
            # I'm the peer with the smallest id
            if hash > self.get_pre("first") or hash <= self.get_myid():
                # the file should be stored here if exists because we have already
                # traverse the whole cycle
                return True
        # I'm not responsible for such file
        return False

    # check if I should store such file
    # check if whis peer will be my suc or not? join()
    def join_me(self,peer_id):
        suc_id = self.get_suc("first")
        if self.my_id < suc_id:
            # I'm not the peer with largest id
            if peer_id > self.my_id and peer_id < suc_id:
                return True
            return False
        elif self.my_id > suc_id:
            # I'm the peer with the largest id
            if peer_id > self.my_id:
                return True
            return False

if __name__ == "__main__":
    

    # test join 
    # 1-2-3-4-5-1
    p1 = peer(1)
    p1.add_suc("first",2)
    p1.add_suc("second",3)
    p1.print_successors()

    p2 = peer(2)
    p2.add_suc("first",3)
    p2.add_suc("second",4)
    
    p3 = peer(3)
    p3.add_suc("first",4)
    p3.add_suc("second",5)

    p4 = peer(4)
    p4.add_suc("first",5)
    p4.add_suc("second",1)
    
    p5 = peer(5)
    p5.add_suc("first",1)
    p5.add_suc("second",2)

    # cant let it join
    print("testing peer 10 ask 2 to join...")
    if (not p2.join_me(10)):
        print("PASS\n")
    else:
        print("FAIL\n")

    # join me
    print("testing peer 10 ask 5 to join...")
    if (p5.join_me(10)):
        print("PASS\n")
    else:
        print("FAIL\n")
    

    # test case 
    """
    test if only one peer
    """
    p = peer(0)
    p.add_suc("first",0)
    p.add_suc("second",0)
    p.add_pre("first",0)
    p.add_pre("second",0)
    
    print("\ntest assign suc and pre...")
    if p.successor["first"] ==\
        p.successor["second"] ==\
            p.predecessor["first"]==\
                p.predecessor["second"] == 0:
                print("Pass")
    else:
        print("suc and pre failed")
    
    print("\n==========================")
    print("test get_pre and get_suc")
    if (p.get_pre("first") == p.get_pre("second") == 0):
        print("pass")
    else:
        print("get_x failed")

    print("\n==========================")
    print("test has_file")
    if (p.has_file(0)):
        print("Pass")
    else:
        print("has file failed")


    """
    test four peers
    """
    p0 = peer(0)
    p0.add_suc("first",1)
    p0.add_suc("second",2)
    p0.add_pre("first",3)
    p0.add_pre("second",2)
    
    p1 = peer(1)
    p1.add_suc("first",2)
    p1.add_suc("second",3)
    p1.add_pre("first",0)
    p1.add_pre("second",3)
    
    p2 = peer(2)
    p2.add_suc("first",3)
    p2.add_suc("second",0)
    p2.add_pre("first",1)
    p2.add_pre("second",0)

    p3 = peer(3)
    p3.add_suc("first",0)
    p3.add_suc("second",1)
    p3.add_pre("first",2)
    p3.add_pre("second",1)
    
    print("\n==========================")
    print("test get_pre and get_suc")
    if (p0.get_pre("first") == 3 and p0.get_pre("second") == 2):
        print("pass")
    else:
        print("p0 get_x failed")

    print("\n==========================")
    print("test has_file")

    # 0 has 32
    if (p0.has_file(256)):
        print("Pass")
    else:
        print("p0 has_file failed")

    # 1 dont have 12
    if (not p1.has_file(12)):
        print("Pass")
    else:
        print("p1 doesn't has_file failed")
    
    # 2 has 258
    if (p2.has_file(258)):
        print("Pass")
    else:
        print("p2 has_file failed")

    if (p3.has_file(256*3+3)):
        print("Pass")
    else:
        print("p3 has_file failed")