import socket
from TTT import *
from data import Data

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 65432
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

listening = False
insertTurn = False
playing = False


def send(bin_data):
    client.send(bin_data)

def requestStart(playerName):
    data = Data()
    data.action = ACT_START
    data.option = UNDEFINED
    data.size = len(playerName)
    data.data = playerName
    
    bin_data = serialize(data)
    send(bin_data)

def requestMatch():
    data = Data()
    data.action = ACT_MATCH
    data.option = MATCH_REQ
    data.data = " "
    data.size = len(data.data)
    
    bin_data = serialize(data)
    send(bin_data)
    
    global listening
    listening = True
    listen ()
    
def requestSelect(x, y):
    data = Data()
    data.action = ACT_PLAY
    data.option = PLAY_REQ
    data.data = (x, y)
    data.size = len(data.data)
    
    bin_data = serialize(data)
    send(bin_data)
    
    global listening
    listening = True
    listen()
    
def requestFinish():
    data = Data()
    data.action = ACT_FINISH
    data.option = UNDEFINED
    
    bin_data = serialize(data)
    send(bin_data)
    
    client.close()

def readReply():
        global listening
        global insertTurn
        global playing
    # try:
        bin_data = client.recv(MAX_SIZE)
        if bin_data:
            data = deserialize(bin_data)
            if data.action == ACT_MATCH:
                if data.option == MATCH_REP:
                    if data.data[0] == " " and data.data[1] == "wait":
                        print("You are in queue, please wait for another player.")
                    else:
                        print(f"You are {data.data[0]}. Your opponent is \"{data.data[1]}\".")
                        
                        playing = True
                        
                        if data.data[0] == "X":
                            insertTurn = True
                            listening = False
                            
                        printBoard([" " for i in range(9)])
                    
            if data.action == ACT_PLAY:
                if data.option == PLAY_REP:
                    
                    printBoard(data.data)
                    
                    insertTurn = not insertTurn
                    print(insertTurn)
                    
                    if insertTurn :
                        listening = False
                    else :
                        listening = True
                        
                        
                    listen()
                        
                if data.option == PLAY_ERR:
                    print(f"[ERROR]: {data.data}")
                    # code for re enter
                
                return data
            
            if data.action == ACT_REPORT:
                board = data.data[0]
                score = data.data[1]
                status = data.data[2]
                
                printBoard(board)
                
                print()
                print(f"[RESULT] You {status}, you have total win {score}")
                
                playing = False
                
                return data
                    
                        
        
    # except Exception as e:
    #     print(f"[ERROR] {e}")
    #     return None
    
def printBoard(board):
    for i in range(len(board)):
        if i % 3 == 0 :
            print()
        print(f"[{board[i]}]", end="")
    
    print()
    
def listen():
    # Listening for server replies
    global listening
    while listening:
        data = readReply()
        if data:
            listening = False
    

def play():
    global playing
    while playing :
        try :
            x = int(input("Input \"x\" position: "))
            y = int(input("Input \"y\" position: "))
            
            if (x > 2 or x < 0) or (y > 2 and y < 0) :
                print("Please enter number between (0-2, 0-2)")
                continue
            
            requestSelect(x, y)
        except ValueError as e :
            print("Please insert integer value (0-2, 0-2)")
    
player_name = input("Enter your player name to play: ")
requestStart(player_name)

input("Press Enter to request a match...")
requestMatch()
play()

continue_play = input("Do you want another game? [Yes]/[No]: ")
while continue_play.lower() == "yes" :
    requestMatch()
    play()
    continue_play = input("Do you want another game? [Yes]/[No]: ")
    
requestFinish()
    
# input("Press Enter to request a match...")
# requestSelect(5, 1)

# listening = True
# listen()

# working = True
# while working :
#     i = input("command")
#     if i == " " :
#         break
    
