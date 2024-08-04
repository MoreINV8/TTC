from model.player import Player
from controller.game_controller import GameController

if __name__ == "__main__" :
    p1 = Player("X")
    p2 = Player("O")
    controller = GameController(player1=p1, player2=p2)
    controller.check()
    print()
    controller.select(player=p1, x=1, y=1)
    controller.select(player=p1, x=2, y=1)
    controller.select(player=p1, x=0, y=1)
    controller.check()
    controller.resetBoard()
    controller.check()