from model.player import Player
from model.board import Board

class GameController :
    def __init__(self, player1:Player, player2:Player) -> None:
        self.score:dict[Player,int] = {player1:0, player2:0}
        self.board:Board = Board()
        
    def select(self, player:Player, x:int, y:int) -> None:
        if x < 3 and y < 3 and self.board.available(i=y, j=x) :
            self.board.insert(player=player, i=y, j=x)
        elif x >= 3 or y >= 3 :
            print("error index must enter (0-2, 0-2)")
        else :
            print("non-available position")
        
    def check(self) -> None:
        self.board.printBoard()
        v = self.checkVertical()
        h = self.checkHorizontal()
        c = self.checkCross()
        print("Vertical: " + ("NO winner" if v == None else v.mark + " is winner"))
        print("Horizontal:" + ("NO winner" if h == None else h.mark + " is winner"))
        print("Cross:" + ("NO winner" if c == None else c.mark + " is winner"))
        
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
    
    def resetBoard(self) -> None:
        self.board.reset()