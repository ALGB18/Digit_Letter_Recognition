"""
Este modulo contendra todo lo relativo a la interfaz
y a la interaccion con el usuario
"""
import numpy as np
import PIL
from PIL import Image, ImageTk, ImageDraw
from tkinter import ttk
from tkinter import *
from keras.preprocessing import image
from keras.preprocessing.image import load_img
import digit_letter_recognition as dlr


class Interface:
    """
    Clase que establece la interfaz
    """
    def __init__(self, window):
        self.window = window
        self.width = 28
        self.height = 28
        self.frame = LabelFrame(self.window, text="Draw a digit")
        self.frame.grid(row=0, column=0, columnspan=3, pady=10)
        self.canvas = Canvas(self.frame, width=self.width, height=self.height, bg='white')
        self.canvas.grid(row=1, column=0)
        self.canvas.bind("<B1-Motion>", self.paint)
        self.button = Button(self.frame, text="Save and evaluate digit", command=self.predict)
        self.button.grid(row=2, column=0)
        self.result_label = Label(self.frame, text="")
        self.result_label.grid(row=3, column=0)
        self.image = PIL.Image.new("L", (self.width, self.height), 0x0)
        self.draw = PIL.ImageDraw.Draw(self.image)

        self.digit_letter_recognition = dlr.DigitLetterRegognition()


    def paint(self, event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        self.canvas.create_oval(x1, y1, x2, y2, fill="black", width=3)
        self.draw.line([x1, y1, x2, y2], fill="white", width=5)
    def predict(self):
        filename = "image.png"
        self.image.save(filename)
        self.draw.rectangle([0, 0, self.width, self.height], fill="black")
        self.canvas.delete("all")
        image_to_predict = image.load_img("image.png", color_mode="grayscale", 
                                          target_size=(self.width, self.height))
        image_to_predict = image.img_to_array(image_to_predict)
        image_to_predict = np.expand_dims(image_to_predict, axis=0)
        result = self.digit_letter_recognition.model.predict(image_to_predict)
        self.result_label['text'] = "Valor escrito = {}".format(np.argmax(result))






if __name__ == '__main__':
    window = Tk()
    interface = Interface(window)
    window.mainloop()
