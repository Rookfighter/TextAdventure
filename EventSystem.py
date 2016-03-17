import collections

class Event:

    def __init__(self, t, param):
        self.type = t
        self.param = param

class EventSystem:

    def __init__(self, player, rooms, tuiSystem):
        self.__player = player
        self.__rooms = rooms
        self.__tuiSystem = tuiSystem
        self.__eventQueue = collections.deque()

        self.__eventHandlers = {
            'message':self.__messageHandler,
            'changeLock':self.__changeLockHandler,
            'addObject':self.__addObjectHandler,
            'endGame':self.__endGameHandler
        }

    def __messageHandler(self, param):
        self.__tuiSystem.printMessage(param['message'])
        return True

    def __changeLockHandler(self, param):
        room = self.__rooms[param['room']]
        for direction in room.directions:
            if direction['name'] == param['direction']:
                direction['locked'] = param['locked']
                roomName = self.__rooms[direction['room']].name
                self.__tuiSystem.printChangeDoorLock(roomName, param['locked'])
                return True
        return False

    def __addObjectHandler(self, param):
        room = self.__rooms[param['room']]
        room.objects.append(param['object'])
        self.__tuiSystem.printObjectAdded(param['object']['name'])
        return True

    def __endGameHandler(self, param):
        return False

    def update(self):
        while self.__eventQueue:
            event = self.__eventQueue.popleft()
            if not event.type in self.__eventHandlers:
                continue

            if not self.__eventHandlers[event.type](event.param):
                return False
        return True

    def getEventQueue(self):
        return self.__eventQueue