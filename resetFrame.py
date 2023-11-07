import numpy as np
from serialCom import move_row, move_frame

try:
    import tkinter as tk                # python 3
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk     # python 2
    import tkFont as tkfont  # python 2
from constants import reset_width, reset_height   

class ResetFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.geo = str(reset_width) + "x" + str(reset_height)

        label = tk.Label(self, text="Reset SPEERLoom", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Move all motors down", command=lambda: self.all_down())
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))

        button1.pack()
        button.pack()

    def all_down(self):
        move_row(np.zeros((self.controller.num_motors)))
        move_frame(np.zeros((self.controller.num_frames), dtype='int'))
