# have to change type str to Player form src.model.player
class Data :
    def __init__(self) -> None:
        self.action:int = -1
        self.option:int = -1
        self.size:int = 0
        self.data = None
        
    def printData(self) -> None :
        print(self.action, self.option, self.size, self.data)