import numpy as np
from matplotlib import pyplot as plt
import random
from sklearn import preprocessing
from model import *
class Player:

    def __init__(self, id):
        self.id = id
        self.name = ""
        self.category_index = 0
        self.score = 0
        self.ready = False
        self.finished = False

    def next_category(self):
        """
        Increment the category index the player is currently drawing.
        """
        self.category_index += 1

    def increase_score(self, increase):
        """
        Increase the score of the player.
        """
        self.score += increase

    def reset(self):
        """
        Reset the ready status to false, the score and catergory index to 0.
        """
        self.category_index = 0
        self.score = 0
        self.ready = False
        self.finished = False


class Game:
    def __init__(self, id, number_of_players):
        self.number_of_players = number_of_players
        self.players = {}
        self.id = id
        self.categories = np.load("backend/model/categories.npz")["categories"]
        random.shuffle(self.categories)
        self.index = 0
        self.started = False
        self.game_model = ClassficicationModel()

    def add_player(self, player):
        """
        Add the player to the game.
        :param player: The player to be added to the game.
        """
        self.players[player.id] = player

    def set_name(self, player, name):
        """
        Set the name of the player.
        :param player: The player whose name is to be set.
        """
        player.name = name
    def ready(self, player):
        """
        Update the status of the player to ready.
        :param player: The player whose status needs to be updated.
        """
        player.ready = True

    def all_ready(self):
        """
        Check if all the players are ready.
        :return: True if all the players are ready, False otherwise.
        """
        for key in self.players:
            if not self.players[key].ready:
                return False
        return True

    def finished(self, player):
        """
        Update the status of the player to finished.
        :param player: The player whose status needs to be updated.
        """
        player.finished = True

    def all_finished(self):
        """
        Check if all the players are finished.
        :return: True if all the players are finished, False otherwise.
        """
        for key in self.players:
            if not self.players[key].finished:
                return False
        return True

    def reset(self):
        """
        Reset the ready status of all the players.
        """
        for key in self.players:
            self.players[key].reset()
        self.started = False

    def get_category(self, player):
        """
        Get the category to be drawn.
        :param player: The player
        :return: The category to be drawn or message "Finished" (no categories left).
        """
        try:
            category = self.categories[player.category_index]
            return category
        except:
            return "Finished"

    def score_drawing(self, player, dimensions, drawing_string):
        """
        Score the drawing.
        :param category: The category that is supposed to be drawn.
        :param dimensions: The dimensions of the canvas.
        :param drawing_string: The drawing to be scored.
        :return next_category: The next category to be drawn or an empty string if the drawing was not accepted.
        """
        x, y = map(int, dimensions.split(","))
        drawing = np.array(list(map(int, drawing_string.split(",")))).reshape(y, x)
        drawing = self.game_model.reshape_img(drawing) == 0

        score = 0
        next_category = ""
        # Add condition to pass into the model the category and the drawing array to get True or False
        if(self.game_model.predict_category(drawing, self.categories[player.category_index])):
            print("IT IS TRUE")
            score = 1
            player.increase_score(score)
            player.next_category()
            next_category = self.get_category(player)

        return next_category

    def get_info(self, player):
        """
        Get the category the player is supposed to draw
        and the current scores of all the players.
        :param player: The player
        """
        if self.all_finished():
            return "Game finished."
        else:
            category = self.get_category(player)

            temp = []
            for key in self.players:
                temp.append(self.players[key].name)
            names = ","
            names = names.join(temp)

            temp = []
            for key in self.players:
                temp.append(str(self.players[key].score))
            scores = ","
            scores = scores.join(temp)

            return f"{category},{names},{scores}"

    def start(self):
        """
        Start the game.
        """
        if len(self.players) == self.number_of_players and self.all_ready():
            self.started = True
