import socket
import threading
from TTT import *
from data import Data

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 12_000

ADDR = (SERVER, PORT)

activate_player = set()
player_data:dict[tuple, dict[str]] = dict()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def listen() -> None:
    print(f"[LISTENING] Server is listening at {SERVER}")
    server.listen()
    while True :
        connection, port = server.accept()
        thread = threading.Thread(target=clientHandle, args=(connection, port))
        thread.start()
        print(f"[ACTIVATING] {threading.active_count() - 1}")
        
def clientHandle(connection:socket.socket, port) :
    print(f"[START ACTIVATED] {port} connected")
    
    conneced = True
    while conneced :
        if connection :
            msg = connection.recv(MAX_SIZE)
            if msg :
                msg = deserialize(msg)
                
                if msg.action == ACT_START :
                    activate_player.add(port)
                    player_data[port] = {
                        "connection": connection,
                        "score": 0,
                        "name": msg.data
                    }
                    
                    print(player_data)
                    
                if msg.action == ACT_FINISH :
                    activate_player.remove(port)
                    player_data.pop(port)
                    conneced = False
                    
                    print(f"[CONNECTION] {port} is disconnected")
    
listen()