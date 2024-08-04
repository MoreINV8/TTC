class Player :
    def __init__(self, mark:str) -> None:
        self.mark:str = mark
        
    def isEqual(self, another:object) -> bool:
        if (isinstance(another, Player) and another.mark == self.mark) :
            return True
        return False