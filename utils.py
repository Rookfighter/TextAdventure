def findObjectByName(objectList, name):
    paramUp = name.upper()
    for it in objectList:
        if it['name'].upper() == paramUp:
            return it
    return None

def defaultRoom(room):
    if room.objects is None:
        room.objects = []
    if room.directions is None:
        room.directions = []
    if room.onUse is None:
        room.onUse = []
    if room.onEnter is None:
        room.onEnter = []

def defaultObject(obj):
    if not 'takeable' in obj:
        obj['takeable'] = False
    if not 'useable' in obj:
        obj['useable'] = False

def defaultDirection(direction):
    if not 'visible' in direction:
        direction['visible'] = True
    if not 'locked' in direction:
        direction['locked'] = False