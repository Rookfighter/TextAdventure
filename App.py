from Player import Player
from TUISystem import TUISystem
from ActionSystem import ActionSystem
from IOSystem import IOSystem

INIT_ROOM = 'entrance'

class App:
    def __init__(self):
        self.__player = Player()
        self.__rooms = dict()

        # systems
        self.__ioSystem = IOSystem(self.__player, self.__rooms)
        self.__tuiSystem = TUISystem(self.__player, self.__rooms)
        self.__actionSystem = ActionSystem(self.__player, self.__rooms, self.__tuiSystem)
        self.__tuiSystem.setActions(self.__actionSystem.getActions())

    def run(self):
        self.__player.room = INIT_ROOM
        while True:
            self.__ioSystem.update()
            actionStr = self.__tuiSystem.update()
            self.__actionSystem.update(actionStr)
