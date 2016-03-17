import io
import json
import os
import utils
from Room import Room

class IOSystem:

    def __init__(self, player, rooms):
        self.__lastRoom = player.room
        self.__player = player
        self.__rooms = rooms
        self.__absPath = os.path.dirname(os.path.realpath(__file__))

    def __loadRoom(self, roomID):
        fileName = '{0}/rooms/{1}.json'.format(self.__absPath, roomID)
        with io.open(fileName) as fp:
            jsObj = json.load(fp)

        room = Room()
        room.id = roomID
        room.name = jsObj['name']
        if 'objects' in jsObj:
            room.objects = jsObj['objects']
        if 'directions' in jsObj:
            room.directions = jsObj['directions']
        if 'onUse' in jsObj:
            room.onUse = jsObj['onUse']
        if 'onEnter' in jsObj:
            room.onEnter = jsObj['onEnter']

        utils.defaultRoom(room)

        for obj in room.objects:
            utils.defaultObject(obj)

        for direction in room.directions:
            utils.defaultDirection(direction)

        self.__rooms[roomID] = room

    def __enterRoom(self, roomID):
        """
        Loads the new current room and all neighouring rooms if they
        haven't been loaded yet.
        """
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