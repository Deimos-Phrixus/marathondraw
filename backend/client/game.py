import numpy as np
import random

class Player:
    def __init__(self, id):
        self.id = id
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
        self.categories = np.load("dataset/categories.npz")["categories"]
        random.shuffle(self.categories)
        self.index = 0
        self.started = False

    def add_player(self, player):
        """
        Add the player to the game.
        :param player: The player to be added to the game.
        """
        self.players[player.id] = player

    def ready(self, player):
        """
        Update the status of the player to ready.
        :param player: The player whose status needs to be updated.
        """
        self.players[player.id].ready = True

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
        self.players[player.id].finished = True

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
        Reset the ready status of all the players
        """
        for key in self.players:
            self.players[key].reset()
        
        self.started = False

    def get_category(self, player):
        """
        Get the category to be drawn
        :return: The category to be drawn or None (no categories left)
        """
        try:
            category = self.categories[player.category_index]
            return category
        except:
            return None

    def score_drawing(self, player, dimensions, drawing_string):
        """
        Score the drawing.
        :param category: The category that is supposed to be drawn.
        :param dimensions: The dimensions of the canvas.
        :param drawing_string: The drawing to be scored.
        :return: The score for the drawing
        """
        x, y = map(int, dimensions.split(","))
        drawing = np.array(list(map(int, drawing_string.split(",")))).reshape(x, y)

        score = 0
        # Add condition to pass into the model the category and the drawing array to get True or False
        if(True):
            score = 1
        
        self.players[player.id].increase_score(score)

    def get_info(self, player):
        if self.all_finished():
            return "Game finished."
        else:
            category = self.get_category(player)
            scores = []
            for key in self.players:
                scores.append(self.players[key].score)
            return f"{category},{scores}"

    def start(self):
        """
        Start the game.
        """
        if not self.started and len(self.players) == self.number_of_players and self.all_ready():
            self.started = True
