class Player :
    def __init__(self, port, mark:str) -> None:
        self.mark:str = mark
        self.port = port
        
    def checkPort(self, another) -> bool:
        return self.port == another
        
    def isEqual(self, another:object) -> bool:
        if (isinstance(another, Player) and another.mark == self.mark) :
            return True
        return False