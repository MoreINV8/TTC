import socket
# from TTT import MAX_SIZE, deserialize, serialize
from TTT import *
from data import Data

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 12_000

ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(ADDR)

def sendData(data:Data) -> None:
    bin_data = serialize(dataObj=data)
    client.send(bin_data)
    
finish = Data()
finish.action = ACT_FINISH
finish.option = UNDEFINED
finish.size = 0
    
start = Data()
start.action = ACT_START
start.option = UNDEFINED

name = input("Input player name: ")

start.data = name
start.size = len(start.data)
    
sendData(start)

input()

sendData(finish)

