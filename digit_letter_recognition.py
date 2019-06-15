"""
Este modulo contiene todo lo relacionado con el
reconocimiento de digitos y letras
"""
import os
import numpy as np
from keras import optimizers

from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.models import model_from_json

from keras.utils.np_utils import to_categorical
from keras.preprocessing.image import ImageDataGenerator, load_img

class DigitLetterRegognition():
    """
    Implementaa las redes neuronales utilizando keras
    (tensorflow backend)
    """
    def __init__(self):
        
        if os.path.isfile("model.json") and os.path.isfile("model.h5"):
            self.load_model()
        else:
            self.load_data()
            self.create_CNN()
            self.train()
            self.save_model()


    def load_data(self):
        (self.x_train, self.y_train), (self.x_test, self.y_test) = mnist.load_data()
        self.num_classes = 10
        self.img_width = self.img_height = 28

        self.x_train = np.reshape(self.x_train, (self.x_train.shape[0], self.img_height, self.img_width, 1))
        self.x_test = np.reshape(self.x_test, (self.x_test.shape[0], self.img_height, self.img_width, 1))
        self.y_train = to_categorical(self.y_train, self.num_classes)
        self.y_test = to_categorical(self.y_test, self.num_classes)

        self.validation_split = 0.2
        self.datagen = ImageDataGenerator(featurewise_center=True,
                                          featurewise_std_normalization=True,
                                          validation_split=self.validation_split, data_format="channels_first")
        self.datagen.fit(self.x_train)
        self.batch_size = 256
        self.data_train = self.datagen.flow(self.x_train, self.y_train, batch_size=self.batch_size, subset="training")
        self.data_dev = self.datagen.flow(self.x_train, self.y_train, batch_size=self.batch_size, subset="validation")
        self.data_test = self.datagen.flow(self.x_test, self.y_test, batch_size=self.batch_size)

    def create_CNN(self):
        self.model = Sequential()

        self.model.add(Conv2D(32, 3, activation='relu', input_shape=(self.img_width, self.img_height, 1)))
        self.model.add(Conv2D(32, 3, activation='relu'))

        self.model.add(MaxPooling2D())

        self.model.add(Conv2D(64, 3, activation='relu'))
        self.model.add(Conv2D(64, 3, activation='relu'))

        self.model.add(MaxPooling2D())

        self.model.add(Flatten())

        self.model.add(Dense(512, activation='relu'))

        self.model.add(Dense(self.num_classes, activation='softmax'))

        self.model.summary()

    def train(self):
        self.model.compile(loss='categorical_crossentropy', optimizer=optimizers.adam(lr=0.001),
                           metrics=['accuracy'])
        
        self.model.fit_generator(self.data_train, epochs=6, verbose=2,
                            steps_per_epoch=len(self.x_train) * (1-self.validation_split) / self.batch_size,
                            validation_data=self.data_dev,
                            validation_steps=len(self.x_train)*self.validation_split/self.batch_size)
        
        print()
        test_loss, test_acc = self.model.evaluate_generator(self.data_test, steps=len(self.x_test)/self.batch_size,
                                                            verbose=1)

        print("test_loss: %.4f, test_acc: %.4f" % (test_loss, test_acc))

    def save_model(self):
        model_json = self.model.to_json()
        with open("model.json", "w") as json_file:
            json_file.write(model_json)
        self.model.save_weights("model.h5")
        print("Saved model to disk")

    def load_model(self):
        json_file = open("model.json", "r")
        loaded_model_json = json_file.read()
        json_file.close()
        self.model = model_from_json(loaded_model_json)
        self.model.load_weights("model.h5")
        print("Loaded model from disk")
