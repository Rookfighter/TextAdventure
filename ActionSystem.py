from EventSystem import Event

class ActionSystem:

    def __init__(self, player, rooms, tuiSystem, eventQueue):
        self.__player = player
        self.__rooms = rooms
        self.__tuiSystem = tuiSystem
        self.__eventQueue = eventQueue

        # a mapping for input actions to functions
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
        """
        Callback for "use" command. Uses an item either from inventory or
        from the current room.
        """
        obj = self.__findObject(param)
        currRoom = self.__rooms[self.__player.room]

        if obj is None:
            self.__tuiSystem.printInvalidObject(param)
            return

        if obj['useable']:
            if not obj['name'] in currRoom.onUse:
                self.__tuiSystem.printNoEffect()
            else:
                events = currRoom.onUse[obj['name']]
                for event in events:
                    self.__eventQueue.append(Event(event['type'], event))
        else:
            self.__tuiSystem.printUnusableObject(obj['name'])

    def __take(self, param):
        """
        Callback for "take" command. Removes a object from the current room
        and adds it to the inventory.
        """
        obj = self.__findObject(param)

        if obj is None:
            self.__tuiSystem.printInvalidObject(param)
            return

        if obj['takeable']:
            self.__rooms[self.__player.room].objects.remove(obj)
            self.__player.inventory.append(obj)
            obj['takeable'] = False
            self.__tuiSystem.printObjectTaken(obj['name'])
        else:
            self.__tuiSystem.printObjectUntakeable(obj['name'])

    def __goto(self, param):
        """
        Callback for "goto" command. Moves to the next room by either specifying
        the direction or the next room name..
        """
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
        """
        Callback for "examine" command. Prints the examine field of an object.
        """
        obj = self.__findObject(param)

        if obj is None:
            self.__tuiSystem.printInvalidObject(param)
        else:
            self.__tuiSystem.printExamine(obj)

    def __inventory(self, param):
        """
        Callback for "inventory" command. Prints the current inventory.
        """
        self.__tuiSystem.printInventory()

    def __room(self, param):
        """
        Callback for "room" command. Prints the current room.
        """
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