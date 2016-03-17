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
            'changeDirection':self.__changeDirectionHandler,
            'endGame':self.__endGameHandler,
            'checkConstraint':self.__checkConstraintHandler
        }

    def __messageHandler(self, param):
        self.__tuiSystem.printMessage(param['message'])
        return True

    def __changeLockHandler(self, param):
        """
        Locks and unlocks doors.
        """
        room = self.__rooms[param['room']]
        for direction in room.directions:
            if direction['name'] == param['direction']:
                direction['locked'] = param['locked']
                roomName = self.__rooms[direction['room']].name
                self.__tuiSystem.printChangeDoorLock(roomName, param['locked'])
                return True
        return False

    def __addObjectHandler(self, param):
        """
        Adds objects to a room.
        """
        room = self.__rooms[param['room']]
        for obj in param['objects']:
            room.objects.append(obj)
            if not 'useable' in obj:
                obj['useable'] = False
            if not 'takeable' in obj:
                obj['takeable'] = False

            self.__tuiSystem.printObjectAdded(obj['name'])
        return True

    def __changeDirectionHandler(self, param):
        """
        Changes the visibility of a door.
        """
        room = self.__rooms[param['room']]
        for direction in room.directions:
            if direction['name'] == param['direction']:
                direction['visible'] = param['visible']
                if direction['visible']:
                    self.__tuiSystem.printDoorFound(direction['name'])
        return True

    def __endGameHandler(self, param):
        """
        Terminates the game.
        """
        self.__tuiSystem.printToBeContinued()
        return False

    def __checkConstraintHandler(self,param):
        """
        Handler for constraints that need to met. If they are not met a
        fail message is printed and the game terminates.
        """
        for obj in self.__player.inventory:
            if obj['name'] == param['item']:
                return True

        self.__tuiSystem.printMessage(param['failMsg'])
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