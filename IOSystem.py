import io
import json
from Room import Room

class IOSystem:

    def __init__(self, player, rooms):
        self.__lastRoom = player.room
        self.__player = player
        self.__rooms = rooms

    def __loadRoom(self, roomID):
        fileName = 'rooms/{0}.json'.format(roomID)
        with io.open(fileName) as fp:
            jsObj = json.load(fp)

        room = Room()
        room.id = roomID
        room.name = jsObj['name']
        room.objects = []
        if 'objects' in jsObj:
            room.objects = jsObj['objects']

        room.onUse = []
        if 'onUse' in jsObj:
            room.onUse = jsObj['onUse']

        room.onEnter = []
        if 'onEnter' in jsObj:
            room.onEnter = jsObj['onEnter']

        for obj in room.objects:
            if not 'takeable' in obj:
                obj['takeable'] = False
            if not 'useable' in obj:
                obj['useable'] = False

        room.directions = jsObj['directions']

        self.__rooms[roomID] = room

    def __enterRoom(self, roomID):
        if not roomID in self.__rooms:
            self.__loadRoom(roomID)
        for direction in self.__rooms[roomID].directions:
            nextRoomID = direction['room']
            if not nextRoomID in self.__rooms:
                self.__loadRoom(nextRoomID)

    def update(self):
        if self.__lastRoom != self.__player.room:
            self.__enterRoom(self.__player.room)
            self.__lastRoom = self.__player.room