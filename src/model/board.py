from model.player import Player

class Board :
    def __init__(self) -> None:
        self.board:list[list[Player]] = []
        self.initBoard()
        
    def initBoard(self) -> None:
        for i in range(3) :
            row = [None for j in range(3)]
            self.board.append(row)
            
    def insert(self, player:Player, i:int, j:int) -> None:
        self.board[i][j] = player
        
    def available(self, i:int, j:int) -> bool:
        return True if self.board[i][j] == None else False
    
    def reset(self) -> None:
        for i in range(len(self.board)) :
            for j in range(len(self.board[i])) :
                self.board[i][j] = None
    
    def getCopyBoard(self) -> list[list[Player]]:
        return self.board.copy()
            
    def printBoard(self) -> None:
        for i in self.board :
            print("{", end="")
            for j in i :
                print("[" + (" " if j == None else j.mark) + "]", end="")
            print("}")