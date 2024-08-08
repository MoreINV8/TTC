import socket
import threading
from TTT import *
from data import Data
from player import Player
from game_controller import GameController

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 65432
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

player_data = {}
matching_queue = []
matching_play = {}

def listen():
    print(f"[LISTENING] Server is listening at {SERVER}")
    server.listen()
    while True:
        connection, address = server.accept()
        thread = threading.Thread(target=clientHandle, args=(connection, address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

def clientHandle(connection, address):
    print(f"[NEW CONNECTION] {address} connected")
    
    connected = True
    while connected:
        # try:
            bin_msg = connection.recv(MAX_SIZE)
            if bin_msg:
                msg = deserialize(bin_msg)

                if msg:
                    if msg.action == ACT_START:
                        if not player_data.get(address) :
                            player_data[address] = {
                                "connection": connection,
                                "score": 0,
                                "name": msg.data
                            }
                        print(f"[PLAYER] {address}, ({player_data[address]['name']})")

                    if msg.action == ACT_MATCH:
                        if msg.option == MATCH_REQ:
                            matching_queue.append(address)
                            if len(matching_queue) >= 2:
                                matchHandle()
                                pass
                            else:
                                waitHandle(address)

                    if msg.action == ACT_PLAY:
                        if msg.option == PLAY_REQ:
                            x = msg.data[0]
                            y = msg.data[1]
                            
                            print(f"{address} is select ({x},{y})")
                            playHandle(address, x, y)
                            
                    if msg.action == ACT_FINISH:
                        player_data.pop(address)
                        connected = False

        # except Exception as e:
        #     print(f"[ERROR] {e}")
        #     connected = False

    connection.close()
    print(f"[DISCONNECTED] {address} disconnected")

def waitHandle(address):
    data = Data()
    data.action = ACT_MATCH
    data.option = MATCH_REP
    data.data = (" ", "wait")
    data.size = len(data.data[1]) + len(data.data[0])
    
    send(address, serialize(data))
    
def matchHandle():
    player1 = matching_queue.pop(0)
    player2 = matching_queue.pop(0)
    
    player1 = Player(port=player1, mark="X")
    player2 = Player(port=player2, mark="O")
    
    game = GameController(player1=player1, player2=player2)
    
    matching_play[player1.port] = game
    matching_play[player2.port] = game
    
    data = Data()
    data.action = ACT_MATCH
    data.option = MATCH_REP
    
    data.data = (player1.mark, player_data[player2.port]["name"])
    data.size = len(player1.mark) + len(player_data[player2.port]["name"])
    send(player1.port, serialize(data))
    
    data.data = (player2.mark, player_data[player1.port]["name"])
    data.size = len(player2.mark) + len(player_data[player1.port]["name"])
    send(player2.port, serialize(data))
    
def playHandle(addr, x, y):
    game:GameController = matching_play[addr]
    
    request_player = game.getPlayer(addr)
    
    print(game.turn)
    
    if game.checkTurn(request_player) :
        canInsert = game.select(x, y)
        
        if canInsert == 0 :
            winner = game.check()
            end_game = game.checkEnd()
            
            if winner :
                winnerHandle(winner, game)
                
            elif end_game :
                endHandle(game)
                
            else: 
                data = Data()
                data.action = ACT_PLAY
                data.option = PLAY_REP
                data.data = game.getBoard()
                data.size = len(data.data)
                
                bin_data_board = serialize(data)
                for player in game.players :
                    send(player.port, bin_data_board)
                
        
        else :
            data = Data()
            data.action = ACT_PLAY
            data.option = PLAY_ERR
            
            if canInsert == -1 :
                data.data = "must insert number in range 0-2"
                data.size = len(data.data)
            if canInsert == -2 :
                data.data = "can't insert this spot"
                data.size = len(data.data)
            
            send(addr, serialize(data))
            
    else :
        data = Data()
        data.action = ACT_PLAY
        data.option = PLAY_ERR
        data.data = "not your turn"
        data.size = len(data.data)
        
        send(addr, serialize(data))
        
def winnerHandle(winner, game:GameController):
    data = Data()
    data.action = ACT_REPORT
    data.option = UNDEFINED
    
    player_data[winner]["score"] += 1
    
    for player in game.players:
        if player.checkPort(winner) :
            data.data = (game.getBoard(), player_data[player.port]["score"], "win")
        
        else :
            data.data = (game.getBoard(), player_data[player.port]["score"], "lose")

        data.size = len(data.data[0]) + 1 + len(data.data[2])
        
        send(player.port, serialize(data))
        
        matching_play.pop(player.port)
        
def endHandle(game:GameController):
    data = Data()
    data.action = ACT_REPORT
    data.option = UNDEFINED
    
    for player in game.players:
        data.data = (game.getBoard(), player_data[player.port]["score"], "draw")
        data.size = len(data.data[0]) + 1 + len(data.data[2])

        send(player.port, serialize(data))
        
        matching_play.pop(player.port)

def send(address, bin_data):
    # try:
        conn = player_data[address]["connection"]
        conn.sendall(bin_data)
    # except KeyError:
    #     print(f"[ERROR] No connection found for {address}")
    # except Exception as e:
    #     print(f"[ERROR] {e}")

print("[STARTING] Server is starting...")
listen()
