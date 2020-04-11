# message passing by through peers

from para import *

# integer to byte converter
def int2byte(num:int):
    return num.to_bytes(8,"big")

# byte to integer
def byte2int(byte:bytes):
    return int.from_bytes(byte,"big")

class message(object):
    def __init__(self,segment = None):
        self.__msg = bytearray()
        self.__seg_size = parameters()["MSG_SIZE"]
        if segment:
            # segment will be the data we want to transfer
            self.segment = segment
    
    def setHeader(self,msg_type,peerid):
        # msg_type is the header type defined in para.py
        self.__msg[0:16] = int2byte(msg_type) + int2byte(peerid)
    
    @property
    def header(self):
        return byte2int(self.__msg[0:8]),byte2int(self.__msg[8:16])
    
    # total segment size
    @property
    def seg_size(self):
        return self.__seg_size

    # actuall msg data length 
    def get_bodySize(self):
        return len(self.__msg) - 16
    
    @property
    def body(self):
        return self.__msg[16:]

    @body.setter
    def body(self,body:bytearray):
        self.__msg[16:self.seg_size+16] = body
    
    @property
    def segment(self):
        return self.__msg

    @segment.setter
    def segment(self,val):
        self.__msg = val

if __name__ == "__main__":
    i = 14
    print(byte2int(int2byte(i)) == i)

    msg = message("hello")
    msg = message()
    msg.setHeader(2, 7)
    msg.body = bytes('helloworld', 'utf-8')
    print(msg.header)
    print(msg.get_bodySize())
    print(msg.seg_size)
    recv = message( msg.segment)
    print(recv.header)
    print(recv.body)
