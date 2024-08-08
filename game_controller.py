from player import Player
from board import Board

class GameController :
    def __init__(self, player1:Player, player2:Player) -> None:
        self.players:list[Player] = [player1, player2]
        self.board:Board = Board()
        self.turn:int = 0
        
    def select(self, x:int, y:int) -> int:
        if x < 3 and y < 3 and self.board.available(i=y, j=x) :
            self.board.insert(player=self.players[self.turn], i=y, j=x)
            
            if self.turn == 0 :
                self.turn = 1
            elif self.turn == 1 :
                self.turn = 0
                
            return 0
        elif x >= 3 or y >= 3 :
            print("error index must enter (0-2, 0-2)")
            return -1
        else :
            print("non-available position")
            return -2
            
    def checkTurn(self, p) -> bool:
        if p == None :
            return False
        return self.players[self.turn].checkPort(p.port)
    
    def getPlayer(self, port) -> Player:
        for p in self.players :
            if p.checkPort(port) :
                return p
        return None
    
    def checkEnd(self):
        count_blank = 0
        for i in self.board.board :
            for j in i :
                if not j:
                    count_blank += 1
                
        return count_blank == 0
        
    def check(self) -> tuple|None:
        self.board.printBoard()
        v = self.checkVertical()
        h = self.checkHorizontal()
        c = self.checkCross()
        print("Vertical: " + ("NO winner" if v == None else v.mark + " is winner"))
        print("Horizontal:" + ("NO winner" if h == None else h.mark + " is winner"))
        print("Cross:" + ("NO winner" if c == None else c.mark + " is winner"))
        
        if v :
            return v.port
        if h :
            return h.port
        if c :
            return c.port
        
        return None
        
    def checkVertical(self) -> Player:
        board = self.board.getCopyBoard()
        
        for i in range(3) :
            checker = board[i][0]
            j = 0
            if checker != None :
                while j < 3 :
                    if  not checker.isEqual(board[i][j]) :
                        break
                    j += 1
            
                if j == 3 :
                    return checker
            
        return None
    
    def checkHorizontal(self) -> Player:
        board = self.board.getCopyBoard()
        
        for j in range(3) :
            checker = board[0][j]
            i = 0
            if checker != None :
                while i < 3 :
                    if not checker.isEqual(board[i][j]) :
                        break
                    i += 1
                
                if i == 3 :
                    return checker
            
        return None
    
    def checkCross(self) -> Player:
        board = self.board.getCopyBoard()
        
        # check for cross from left to right
        i = 0
        j = 0
        checker = board[i][j]
        if checker != None :
            while i < 3 and j < 3 :
                if not checker.isEqual(board[i][j]) :
                    break
                i += 1
                j += 1
                
            if i == 3 and j == 3 :
                return checker
        
        # check for cross from right to left
        i = 0
        j = 2
        checker = board[i][j]
        if checker != None :
            while i < 3 and j >= 0 :
                if not checker.isEqual(board[i][j]) :
                    break
                i += 1
                j -= 1
                
            if i == 3 and j == -1 :
                return checker
        
        return None
    
    def getBoard(self) -> list:
        board = list()
        for i in range(3) :
            for j in range(3) :
                pos = self.board.board[i][j]
                board.append(pos.mark if pos else " ")
                
        return board