import numpy as np
import random


# Player: index_cat, score

class Game:
    def __init__(self, id):
        self.playersReady = [False, False, False, False]
        self.id = id
        self.categories = np.load("backend/model/categories.npz")["categories"]
        random.shuffle(self.categories)
        self.index = 0

    def ready(self, player):
        """
        Update the status of the player to ready.
        :param player: The player whose status needs to be updated.
        """
        self.playersReady[player] = True

    def all_ready(self):
        """
        Check if all the players are ready.
        :return: True if all the players are ready, False otherwise.
        """
        return not (False in self.playersReady)

    def reset_ready(self):
        """
        Reset the ready status of all the players
        """
        for i in range(4):
            self.playersReady[i] = False

    def get_category(self, player):
        """
        Get the category to be drawn
        :return: The category to be drawn or None (no categories left)
        """
        try:
            category = self.categories[self.index]
            self.index += 1
            return category
        except:
            return None

    def score_drawing(self, data):
        """
        Score the drawing.
        :param data: The drawing to be score.
        :return: The score for the drawing
        """
        drawing = pickle.load(data)
        score = random.randint(0, 10)
        return score
