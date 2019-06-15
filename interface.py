"""
Este modulo contendra todo lo relativo a la interfaz
y a la interaccion con el usuario
"""
import PIL
from PIL import Image, ImageTk, ImageDraw
from tkinter import ttk
from tkinter import *

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
        self.button = Button(self.frame, text="Save and evaluate digit", command=self.save)
        self.button.grid(row=2, column=0)
        self.result_label = Label(self.frame, text="")
        self.result_label.grid(row=3, column=0)
        self.image = PIL.Image.new("L", (self.width, self.height), 0xFFFFFF)
        self.draw = PIL.ImageDraw.Draw(self.image)

    def paint(self, event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        self.canvas.create_oval(x1, y1, x2, y2, fill="black", width=3)
        self.draw.line([x1, y1, x2, y2], fill="black", width=5)
    def save(self):
        filename = "image.png"
        self.image.save(filename)



if __name__ == '__main__':
    window = Tk()
    interface = Interface(window)
    window.mainloop()
