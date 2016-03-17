from Player import Player
from TUISystem import TUISystem
from ActionSystem import ActionSystem
from IOSystem import IOSystem
from EventSystem import EventSystem

INIT_ROOM = 'entrance'

class App:
    def __init__(self):
        self.__player = Player()
        self.__rooms = dict()

        # sub systems
        self.__ioSystem = IOSystem(self.__player, self.__rooms)
        self.__tuiSystem = TUISystem(self.__player, self.__rooms)
        self.__eventSystem = EventSystem(self.__player, self.__rooms, self.__tuiSystem)
        self.__actionSystem = ActionSystem(self.__player, self.__rooms, self.__tuiSystem,
                                           self.__eventSystem.getEventQueue())
        self.__tuiSystem.setActions(self.__actionSystem.getActions())

    def __run(self):
        self.__player.room = INIT_ROOM
        while True:
            self.__ioSystem.update()
            actionStr = self.__tuiSystem.update()
            self.__actionSystem.update(actionStr)
            if not self.__eventSystem.update():
                break

    def run(self):
        try:
            self.__run()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(e)

        print('')
        raw_input('Press RETURN...')