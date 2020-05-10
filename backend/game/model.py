import os
# import random
import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt

from PIL import Image

class ClassficicationModel:
    def __init__(self, model_name="model_opt.h5"):
        print(os.listdir())
        self.model = tf.keras.models.load_model("backend/model/model_opt.h5")
        self.categories = np.load("backend/model/categories.npz")['categories']

    def predict_category(self, input_img):
        # assert input_img.shape[0] == 28
        # assert input_img.shape[1] == 28
        # assert np.max(input_img) == 1
        # assert np.min(input_img) == 0
        
        return self.categories[np.argmax(self.model.predict(input_img))]
    

    def reshape_img(self, input_img):
        """
        Reshapes given image into 28 x 28 image, making it suitable for the model

        :input_img: Image array of any size. 
        :return: Return image array of shape 28 x 28
        """
        img = Image.fromarray(input_img)
        img = img.resize((28,28))
        return np.array(img)

    def normalize_img(self, input_img):
        """
        Normalize all values by dividing 255. Bring values
        between 0-1. 

        :input_img: Image array, should be the original with color values 0-255
        :return: Image array, color values normalized and scaled down between 0-1
        """
        return input_img/255
    
    def invert_color(self, input_img):
        """
        Takes image converting all black points to white
        and rest pints to 0.

        :input_img: Image array
        :return: Image array converting all black points (0) to 1 and rest to 0 (white).
        """
        return input_img == 0

    def process_img(self, input_img):
        input_img = self.reshape_img(input_img)
        input_img = self.normalize_img(input_img)
        input_img = self.invert_color(input_img)
        return input_img
if __name__ == "__main__":
    classifier = ClassficicationModel()
    mistakes = 0
    fig=plt.figure(figsize=(10, 10))
    columns = 10
    rows = 10
    i = 1
    mis_predictions = []
    for each in classifier.categories:
        datafiles = np.load("training/data/"+each)

        random_img = datafiles[np.random.randint(13000, 23000)]
        random_img = classifier.process_img(random_img.reshape(28, 28))
        input_img = random_img.reshape(1, 28, 28, 1)
        fig.add_subplot(rows, columns, i)
        print(random_img.shape)
        cmap='viridis'
        if each != classifier.predict_category(input_img):
            print("Error predicting", each)
            mistakes += 1
            mis_predictions.append(each)
        else:
            # print("Correctly predicted")
            cmap='gray'

        
        
        plt.imshow(random_img, cmap=cmap)
        plt.axis('off')
        i += 1
    print("Total mispredictions", mistakes, mistakes/len(classifier.categories))
    print(mis_predictions)
    plt.show()