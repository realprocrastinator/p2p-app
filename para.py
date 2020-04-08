
class parameters(dict):
    """
    store the basic parameters for later usage
    PORT_BASE = 12000
    PEER_ID
    PING_INTERVAL
    """
    __para = {
        "PORT_BASE" : 12000, # port = base + peer_id
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
