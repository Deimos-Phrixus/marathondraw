import numpy as np
from matplotlib import pyplot as plt
import math
import os
import plaidml.keras
plaidml.keras.install_backend()
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
from keras import backend as K
from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense, Dropout
from keras.callbacks import ModelCheckpoint


class Classifier:
    
    def __init__(self, model):
        if model=="" or type(model) != str:
            return "Model should have a name"
        try:
            self.model = load_model(model)
            print("Loaded old model")
        except:
            self.model = Classifier.create_model()
            print("New model created")
        self.model_name = model
        self.batch_size = 512
        
    def get_model(self):
        return self.model
    
    def create_model():
        model = Sequential()
        model.add(Dropout(0.2, input_shape=(28,28,1)))
        model.add(Conv2D(32,kernel_size=7,padding='same',activation='relu'))
        model.add(MaxPool2D())
        model.add(Conv2D(64,kernel_size=5,padding='same',activation='relu'))
        model.add(MaxPool2D())
        model.add(Conv2D(128,kernel_size=3,padding='same',activation='relu'))
        model.add(MaxPool2D())
        model.add(Flatten())
        model.add(Dense(256, activation='relu'))
        model.add(Dense(100, activation='softmax'))
        model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
        return model
    
    def XY_Gen(self, files):
        while True:
            np.random.shuffle(files)
            for each in files:
                dataset = np.load("../dataset/"+each)['dataset']
                np.random.shuffle(dataset)
                X = dataset[:, :784]
                Y = dataset[:, 784:]
                X = X.reshape((X.shape[0], 28, 28, 1))
                for i in range(0, X.shape[0], self.batch_size):
                    yield(X[i:min(i+self.batch_size, X.shape[0])], Y[i:min(i+self.batch_size, X.shape[0])])
                del X, Y, dataset
    
    def fit_model(self,train_files, epochs=10):
        print("Starting model training")
        self.model.fit_generator(self.XY_Gen(train_files), epochs=epochs, steps_per_epoch=math.ceil((1000_000)//self.batch_size), verbose=1, callbacks=[ModelCheckpoint(self.model_name, monitor='acc', save_best_only=True)])
    
train_files = []
test_files = []
for each in os.listdir("../dataset"):
    if "testing" in each:
        test_files.append(each)
    elif "training" in each:
        train_files.append(each)

model_names = ["modelv1.h5", "modelv2-largerconvlayers.h5"]
selected_model = model_names[1]
classifier = Classifier(selected_model)
classifier.fit_model(train_files)