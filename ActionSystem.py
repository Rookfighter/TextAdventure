class ActionSystem:

    def __init__(self, player, rooms, tuiSystem):
        self.__player = player
        self.__rooms = rooms
        self.__tuiSystem = tuiSystem

        self.__actions = {
            'use': self.__use,
            'take': self.__take,
            'goto': self.__goto,
            'examine': self.__examine,
            'inventory':self.__inventory,
            'room': self.__room
        }

    def __findObject(self, param):
        currRoom = self.__rooms[self.__player.room]
        paramUp = param.upper()

        for obj in currRoom.objects:
            if obj['name'].upper() == paramUp:
                return obj

        for obj in self.__player.inventory:
            if obj['name'].upper() == paramUp:
                return obj

        return None

    def __findDirection(self, param):
        currRoom = self.__rooms[self.__player.room]
        paramUp = param.upper()

        for direction in currRoom.directions:
            roomName = self.__rooms[direction['room']].name
            if paramUp ==  direction['name'].upper() or paramUp == roomName.upper():
                return direction
        return None


    def __use(self, param):
        pass

    def __take(self, param):
        obj = self.__findObject(param)

        if obj is None:
            self.__tuiSystem.printInvalidObject(param)
            return

        if obj['takeable']:
            self.__rooms[self.__player.room].objects.remove(obj)
            self.__player.inventory.append(obj)
            obj['takeable'] = False
            self.__tuiSystem.printObjectTaken(param)
        else:
            self.__tuiSystem.printObjectUntakeable(param)

    def __goto(self, param):
        direction = self.__findDirection(param)

        if direction is None:
            self.__tuiSystem.printInvalidDirection(param)
            return

        if direction['locked']:
            self.__tuiSystem.printDoorLocked()
        else:
            self.__player.room = direction['room']
        return

    def __examine(self, param):
        obj = self.__findObject(param)

        if obj is None:
            self.__tuiSystem.printInvalidObject(param)
        else:
            self.__tuiSystem.printExamine(obj)

    def __inventory(self, param):
        self.__tuiSystem.printInventory()

    def __room(self, param):
        self.__tuiSystem.printRoom(self.__player.room)

    def getActions(self):
        return self.__actions.keys()

    def update(self, actStr):
        self.__player.action = None
        action = actStr
        param = ''

        idx = actStr.find(' ')
        if idx > 0:
            action = actStr[:idx]
            param = actStr[idx+1:]

        if not action in self.__actions:
            self.__tuiSystem.printInvalidAction(action)
            return

        self.__actions[action](param)