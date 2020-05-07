import numpy as np
import os
import plaidml.keras
import os
plaidml.keras.install_backend()
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
from keras import backend as K
from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense, Dropout

dataset_filenames = os.listdir("dataset/")
categories = np.load("dataset/categories.npz")['categories']
X_train_set = []
Y_train_set = []
X_test_set = []
Y_test_set = []
for each in dataset_filenames:
    if 'test' in each:
        test_data = np.load("dataset/"+each)
        X_test_set.append(test_data['X_test'])
        Y_test_set.append(test_data['Y_test'])
    elif 'train' in each:
        train_data = np.load("dataset/"+each)
        X_train_set.append(train_data['X_train'])
        Y_train_set.append(train_data['Y_train'])
X_train = np.concatenate(X_train_set)
Y_train = np.concatenate(Y_train_set)
X_test = np.concatenate(X_test_set)
Y_test = np.concatenate(Y_test_set)

class Classifier:
    
    def __init__(self, model=None):
        self.model = model
        
    def get_model(self):
        return self.model
    
    def create_model():
        model = Sequential()
        model.add(Dropout(0.2, input_shape=(28,28,1)))
        model.add(Conv2D(32,kernel_size=7,padding='same',activation='relu'))
        model.add(MaxPool2D())
        model.add(Conv2D(64,kernel_size=3,padding='same',activation='relu'))
        model.add(MaxPool2D())
        model.add(Flatten())
        model.add(Dense(256, activation='relu'))
        model.add(Dense(10, activation='softmax'))
        model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
        return model
    
    def fit_model(self, X_train, Y_train, X_test, Y_test, epochs=5, batch_size=256):
        print("Starting model training")
        print("Loss values before training with test data:", self.model.evaluate(X_test, Y_test))
        self.model.fit(x=X_train, y=Y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1, verbose=1)
        print("Loss values after training with test data:", self.model.evaluate(X_test, Y_test))


X_train = X_train.reshape((X_train.shape[0], 28, 28, 1))
X_test = X_test.reshape((X_test.shape[0], 28, 28, 1))

classifer = Classifier(Classifier.create_model())

classifer.fit_model(X_train, Y_train, X_test, Y_test, batch_size=512, epochs=100)