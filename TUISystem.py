class TUISystem:

    def __init__(self, player, rooms):
        self.__lastRoom = player.room
        self.__player = player
        self.__rooms = rooms
        self.__actions = []

    def printFramedOutput(self, lines):
        # find longest line
        maxLen = 0
        for l in lines:
            if len(l) > maxLen:
                maxLen = len(l)

        # create box header
        f = ['+']
        for _ in range(maxLen + 2):
            f.append('-')
        f.append('+')

        # pad lines with spaces
        toPrint = [''.join(f)]
        for l in lines:
            tmp = ['| ', l]
            for _ in range(maxLen - len(l)):
                tmp.append(' ')
            tmp.append(' |')
            toPrint.append(''.join(tmp))

        # print everything
        toPrint.append(''.join(f))
        for l in toPrint:
            print(l)

    def __promptAction(self):
        print('')
        lines = ['What do you want to do?',
                 'Actions: {0}'.format(', '.join(self.__actions))]
        self.printFramedOutput(lines)
        result = raw_input('> ')
        while result == '':
            result = raw_input('> ')
        print('')
        return result

    def update(self):
        if self.__lastRoom != self.__player.room:
            self.__enterRoom(self.__player.room)
            self.__lastRoom = self.__player.room

        return self.__promptAction()

    def __enterRoom(self, roomID):
        room = self.__rooms[roomID]
        print('You entered room {0}.'.format(room.name))
        self.printRoom(roomID)

    def printRoom(self, roomID):
        room = self.__rooms[roomID]
        if room.objects:
            print('The room contains:')
            for obj in room.objects:
                print('* {0} - {1}'.format(obj['name'], obj['description']))
        else:
            print('The room is empty.')

        if room.directions:
            print('You can leave the room')
            for direction in room.directions:
                if not direction['visible']:
                    continue
                roomName = self.__rooms[direction['room']].name
                print('* to the {0} and enter {1}'.format(direction['name'], roomName))

    def setActions(self, actions):
        self.__actions = actions

    def printInventory(self):
        if self.__player.inventory:
            print('Your inventory contains:')
            for obj in self.__player.inventory:
                print('* {0} - {1}'.format(obj['name'], obj['description']))
        else:
            print('Your inventory is empty.')

    def printExamine(self, obj):
        print(obj['examine'])

    def printInvalidDirection(self, direction):
        print('Invalid direction "{0}". Specify either direction or room name.'.format(direction))

    def printInvalidAction(self, action):
        print('Invalid action "{0}".'.format(action))

    def printInvalidObject(self, objectName):
        print('Invalid object "{0}".'.format(objectName))

    def printDoorLocked(self):
        print('The door is locked.')

    def printObjectTaken(self, objectName):
        print('{0} taken.'.format(objectName))

    def printObjectAdded(self, objectName):
        print('New object {0} added.'.format(objectName))

    def printObjectUntakeable(self, objectName):
        print('{0} cannot be taken.'.format(objectName))

    def printUnusableObject(self, objectName):
        print('{0} cannot be used.'.format(objectName))

    def printNoEffect(self):
        print('Nothing happens.')

    def printMessage(self, message):
        print(message)

    def printChangeDoorLock(self, roomName, locked):
        lockStr = 'unlocked'
        if locked:
            lockStr = 'locked'
        print('The door to {0} was {1}.'.format(roomName, lockStr))

    def printDoorFound(self, doorName):
        print('Door to the {0} found.'.format(doorName))

    def printToBeContinued(self):
        print('To be continued...')