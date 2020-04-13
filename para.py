from enum import Enum, unique

@unique
class header(Enum):
    ACK_PING = 0
    SND_PING = 1
    REQ_FILE = 2
    SND_FILE = 3
    FILE_STR = 4
    FILE_ACK = 5
    FILE_REQ = 6
    FILE_RCV = 7
    NEW_PEER = 8
    # gracefully exit
    PEER_EXIT = 9
    PEER_EXIT_ACK = 10
    PEER_LOST = 11
    PEER_JOIN = 12
    JOIN_UPDATE = 13
    JOIN_ALLOWED = 14

def signal(x:Enum):
    return x.value

@unique
class signature(Enum):
    FIRST = 0
    SECOND = 1

class parameters(dict):
    """
    store the basic parameters for later usage
    PORT_BASE = 12000
    PEER_ID
    PING_INTERVAL
    """
    __para = {
        "PORT_BASE" : 12000, # port = base + peer_id
        "HOST_ADDR" : "127.0.0.1",
        "MSG_SIZE" : 1024,  # msg segment size
    }

    def __new__(cls):
        return cls.__para

class uargs(dict):
    """
    store the user input args
    """
    __args = {
        "OPTIONS" : None,   # OPTIONS stored command line options: join|init
        "PEER_ID" : None,
        "FIRST_SUCCESSOR" : None,
        "SECOND_SUCCESSOR" : None,
        "PING_INTERVAL" : None,
        "KNOWN_PEER" : None,
    }

    def __new__(cls):
        return cls.__args


if __name__ == "__main__":
    # print(repr(header.ACK_PING))
    print(signal(header.ACK_PING))