class Game:
    def __init__(self, id):
        self.playersReady = [False, False, False, False]
        self.id = id

    def ready(self, player):
        self.playersReady[player] = True

    def allReady(self):
        return not False in self.playersReady

    def resetReady(self):
        for i in range(4):
            self.playersReady[i] = False