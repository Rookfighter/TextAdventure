class Room:
    def __init__(self):
        self.name = '<unknown>'
        self.objects = None
        self.directions = None
        self.actions = None
        self.onUse = None
        self.onEnter = None