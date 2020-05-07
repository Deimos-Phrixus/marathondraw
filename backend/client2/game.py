import numpy as np
import random


class Game:
    def __init__(self, id):
        self.playersReady = [False, False, False, False]
        self.id = id
        self.categories = np.load("dataset/categories.npz")["categories"]
        random.shuffle(self.categories)

    def ready(self, player):
        self.playersReady[player] = True

    def all_ready(self):
        return not (False in self.playersReady)

    def reset_ready(self):
        for i in range(4):
            self.playersReady[i] = False
