from data import Data
from struct import pack
# DEFINED HEADER

MIN_SIZE = 3
MAX_SIZE = 255
# why 255 because byte size can be contain only maximum 255 in decimal

# FIRST BYTE
ACT_START =         0X00
ACT_MATCH =         0X01
ACT_PLAY =          0X02
ACT_REPORT =        0X03
ACT_FINISH =        0X04

MATCH_REQ =         0X00
MATCH_REP =         0X01

PLAY_REQ =          0X00
PLAY_REP =          0X01
PLAY_ERR =          0XFF

UNDEFINED =         0XFF

# SECOND BYTE IS THE SIZE OF PACKET

# ELSE IS THE DATA

HEADER_ACT = 0
HEADER_OPT = 1
HEADER_SIZE = 2
FIRST_DATA = 3

ACTION = [ACT_START, ACT_MATCH, ACT_PLAY, ACT_REPORT, ACT_FINISH]
MATCH = [MATCH_REQ, MATCH_REP]
PLAY = [PLAY_REQ, PLAY_REP, PLAY_ERR]


def checkValidData(dataObj:Data) -> bool:
    # data have a data
    # data have same size as attb size
    # size of data is less than 256 (<= 255)
    return dataObj.data and (dataObj.size == len(dataObj.data)) and dataObj.size < 256

def checkByteData(packet_list:list[bytes]) -> bool:
    data_size = len(packet_list) - MIN_SIZE
    if packet_list[HEADER_SIZE] != data_size :
        return False
    return True





def serialize(dataObj:Data) -> bytes:
    if dataObj.action not in ACTION :
        return None
    
    if dataObj.action == ACT_START :
        return serializeStart(dataObj=dataObj)
        
    if dataObj.action == ACT_MATCH :
        return serializeMatch(dataObj=dataObj)
        
    if dataObj.action == ACT_PLAY :
        return serializePlay(dataObj=dataObj)
        
    if dataObj.action == ACT_REPORT :
        return serializeReport(dataObj=dataObj)
    
    if dataObj.action == ACT_FINISH :
        return serializeFinish(dataObj=dataObj)
    
def serializeStart(dataObj:Data) -> bytes:
    act_header = pack("B", ACT_START)
    opt_header = pack("B", UNDEFINED)
    
    if not checkValidData(dataObj=dataObj) or not isinstance(dataObj.data, str) :
        return None
    
    size_header = pack("B", dataObj.size)
    
    data = dataObj.data.encode()
    
    return act_header + opt_header + size_header + data

def serializeMatch(dataObj:Data) -> bytes:
    act_header = pack("B", ACT_MATCH)
    
    if dataObj.option not in MATCH :
        return None
    
    if dataObj.option == MATCH_REQ :
        opt_header = pack("B", MATCH_REQ)
        size_header = pack("B", 0)
        
        data = "".encode()
        
    if dataObj.option == MATCH_REP :
        if not dataObj.data or not isinstance(dataObj.data, tuple) or len(dataObj.data[0]) + len(dataObj.data[1])  != dataObj.size:
            return None
        
        opt_header = pack("B", MATCH_REP)
        size_header = pack("B", dataObj.size)
        
        data = dataObj.data[0].encode()
        data += dataObj.data[1].encode()
        
        # data = (client mark, opponent name)
        
    return act_header + opt_header + size_header + data
        
def serializePlay(dataObj:Data) -> bytes:
    act_header = pack("B", dataObj.action)
    
    if dataObj.option not in PLAY :
        return None
    
    if dataObj.option == PLAY_REQ :
        
        if not checkValidData(dataObj=dataObj) :
            return None
        if not isinstance(dataObj.data, tuple) or len(dataObj.data) != 2 :
            return None
        
        opt_header = pack("B", PLAY_REQ)
        size_header = pack("B", dataObj.size)
        
        data = pack("B", dataObj.data[0]) + pack("B", dataObj.data[1])
        
    if dataObj.option == PLAY_ERR :
        
        if not checkValidData(dataObj=dataObj) :
            return None
        if not isinstance(dataObj.data, str) or len(dataObj.data) > MAX_SIZE :
            return None
        
        opt_header = pack("B", PLAY_ERR)
        size_header = pack("B", dataObj.size)
        
        data = dataObj.data.encode()
        
    if dataObj.option == PLAY_REP :
        
        if not checkValidData(dataObj=dataObj) :
            return None
        if not isinstance(dataObj.data, list) or len(dataObj.data) != 9 :
            return None
        
        opt_header = pack("B", PLAY_REP)
        size_header = pack("B", dataObj.size)
        
        data = dataObj.data[0].encode()
        for i in range(1, dataObj.size) :
            data = data + dataObj.data[i].encode()
            
        
    return act_header + opt_header + size_header + data

def serializeReport(dataObj:Data) -> bytes:
    act_header = pack("B", ACT_REPORT)
    
    if not dataObj.data or not isinstance(dataObj.data, tuple) or dataObj.size != 1 + len(dataObj.data[0]) + len(dataObj.data[2]):
        return None
    
    opt_header = pack("B", UNDEFINED)
    size_header = pack("B", 1 + len(dataObj.data[0]) + len(dataObj.data[2]))
    
    data = "".encode()
    for i in dataObj.data[0] :
        data += i.encode()
    
    data += pack("B", dataObj.data[1]) + dataObj.data[2].encode()
    
    # data = (final board, total win, result)
    
    return act_header + opt_header + size_header + data

def serializeFinish(dataObj:Data) -> bytes:
    act_header = pack("B", ACT_FINISH)
    opt_header = pack("B", UNDEFINED)
    size_header = pack("B", 0)
    data = "".encode()
    
    return act_header + opt_header + size_header + data





def deserialize(packet:bytes) -> Data:
    packet_list = list(packet)
    
    if packet_list[HEADER_ACT] not in ACTION or len(packet_list) < MIN_SIZE :
        return None
    
    if packet_list[HEADER_ACT] == ACT_START :
        return deserializeStart(packet_list=packet_list)
    
    if packet_list[HEADER_ACT] == ACT_MATCH :
        return deserializeMatch(packet_list=packet_list)
    
    if packet_list[HEADER_ACT] == ACT_PLAY :
        return deserializePlay(packet_list=packet_list)
    
    if packet_list[HEADER_ACT] == ACT_REPORT :
        return deserializeReport(packet_list=packet_list)
    
    if packet_list[HEADER_ACT] == ACT_FINISH :
        return deserializeFinish(packet_list=packet_list)
    
def deserializeStart(packet_list:list[bytes]) -> Data:
    
    if not checkByteData(packet_list=packet_list) :
        return None
    
    decodedData = Data()
    
    decodedData.action = ACT_START
    decodedData.option = UNDEFINED
    decodedData.size = len(packet_list) - MIN_SIZE
    
    data = ""
    for i in range(FIRST_DATA, MIN_SIZE + decodedData.size) :
        data += chr(packet_list[i])
        
    decodedData.data = data
        
    return decodedData

def deserializeMatch(packet_list:list[bytes]) -> Data:
    decodedData = Data()
    
    decodedData.action = ACT_MATCH
    decodedData.size = len(packet_list) - MIN_SIZE
    
    if packet_list[HEADER_OPT] not in MATCH :
        return None
    
    
    if packet_list[HEADER_OPT] == MATCH_REQ :
        decodedData.option = MATCH_REQ
        
    if packet_list[HEADER_OPT] == MATCH_REP :
        decodedData.option = MATCH_REP
        
        if not checkByteData(packet_list=packet_list) :
            return None
        
        mark = chr(packet_list[FIRST_DATA])
        name = ""
        for i in range(FIRST_DATA + 1, MIN_SIZE + decodedData.size) :
            name += chr(packet_list[i])
            
        decodedData.data = (mark, name)
        
    return decodedData
        
def deserializePlay(packet_list:list[bytes]) -> Data:
    decodedData = Data()
    
    decodedData.action = ACT_PLAY
    decodedData.size = len(packet_list) - MIN_SIZE
    
    if packet_list[HEADER_OPT] not in PLAY :
        return None
    
    if packet_list[HEADER_OPT] == PLAY_REQ :
        
        decodedData.option = PLAY_REQ
        
        if not checkByteData(packet_list=packet_list) :
            return None
        if decodedData.size != 2 :
            return None
        
        x = packet_list[FIRST_DATA + 0]
        y = packet_list[FIRST_DATA + 1]
        
        decodedData.data = (x, y)
        
    if packet_list[HEADER_OPT] == PLAY_ERR :
        decodedData.option = PLAY_ERR
        
        if not checkByteData(packet_list=packet_list) :
            return None
        
        decodedData.size = packet_list[HEADER_SIZE]
        
        data = ""
        for i in range(FIRST_DATA, MIN_SIZE + decodedData.size) :
            data += chr(packet_list[i])
            
        decodedData.data = data
        
    if packet_list[HEADER_OPT] == PLAY_REP :
        decodedData.option = PLAY_REP
        
        if not checkByteData(packet_list=packet_list) :
            return None
        
        data = []
        for i in range(FIRST_DATA, MIN_SIZE + decodedData.size) :
            data.append(chr(packet_list[i]))
            
        decodedData.data = data
        
    return decodedData

def deserializeReport(packet_list:list[bytes]) -> Data:
    decodedData = Data()
    
    decodedData.action = ACT_REPORT
    decodedData.size = len(packet_list) - MIN_SIZE
    decodedData.option = UNDEFINED
    
    if not checkByteData(packet_list=packet_list) :
        return None
    
    board = ""
    for i in range(FIRST_DATA, FIRST_DATA + 9) :
        board += chr(packet_list[i])
        
    score = packet_list[FIRST_DATA + 9]
    
    result = ""
    for i in range(FIRST_DATA + 10, len(packet_list)) :
        result += chr(packet_list[i])
        
    decodedData.data = (board, score, result)
    
    return decodedData

def deserializeFinish(packet_list:list[bytes]) -> Data:
    decodedData = Data()
    
    decodedData.action = ACT_FINISH
    decodedData.option = UNDEFINED
    decodedData.size = len(packet_list) - MIN_SIZE
    
    return decodedData