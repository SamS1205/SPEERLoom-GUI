try:
    import tkinter as tk  # python 3
    from tkinter import ttk # python 3
    from tkinter import font as tkfont  # python 3
    from PIL import ImageTk, Image
except ImportError:
    import Tkinter as tk  # python 2
    import tkFont as tkfont  # python 2
import numpy as np
from constants import *
from constants_info import *


class MathMode_WelcomePage(tk.Frame):

    def __init__(self, parent, controller):
      tk.Frame.__init__(self, parent)
      self.controller = controller
      self.parent     = parent
      self.geo        = str(mathMode_width) + "x" + str(mathMode_height)

      self.rows    = 25
      self.columns = 20 

      #Open Pictures
      self.math_im1       = ImageTk.PhotoImage(Image.open("weaving\weaving_mult_full.png"))

      #Create Labels & Buttons
      label          = tk.Label(self, text="Welcome to Mini Math Mode!", font=controller.title_font).pack()
      label_instr    = tk.Label(self, text=mathMode_instruct, font="Helvetica 12").pack()
      label_instr    = tk.Label(self, text="Math Mode Instructions", font="Helvetica 14 bold underline").pack()
      label_instr_2  = tk.Label(self, text=mathMode_instruct_2, font="Helvetica 12").pack()
      label_instr_3  = tk.Label(self, text=mathMode_instruct_3, font="Helvetica 12 italic").pack()
      math_label_im1 = tk.Label(self, image=self.math_im1, height=330, width=950).pack()
      label_instr_4  = tk.Label(self, text=mathMode_instruct_4, font="Helvetica 12 italic").pack()
      button_back     = tk.Button(self, text="Back", command=lambda: [controller.show_frame("WeaveFrame1")]).pack()
      button_continue = tk.Button(self, text="Continue", command=lambda: [controller.get_page("MathMode_Page1").init_page(),
                                                                          controller.show_frame("MathMode_Page1")]).pack()

      self.pat_row   = 0
      self.highlight = None
      
      #Placing Objects
      """
      label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)
      label_instr.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
      label_instr_2.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
      math_label_im1.place(relx=0.5, rely=0.4)
      label_instr_3.place(relx=0.5, rely=0.6,anchor=tk.CENTER)
      
      button_back.place(relx=0.425, rely= 0.08)
      button_continue.place(relx=0.475, rely= 0.08)
      """

def populate_matrix(canvas, rows, cols, color_background, color_text):
    text = []
    rects = []
    for row in range(rows):
        text_row = []
        rects_row = []
        for column in range(cols):
            x = column * block_size + (column + 1) * buffer
            y = row * block_size + (row + 1) * buffer
            rects_row.append(canvas.create_rectangle(x, y, x + block_size, y + block_size, fill=color_background))
            text_row.append(canvas.create_text(x + block_size / 2, y + block_size / 2, text="0", fill=color_text,
                                               font=('Helvetica 15'), tags=('text_object')))
        text.append(text_row)
        rects.append(rects_row)
    return text, rects

def update_pattern(canvas, text, pattern, tie_upT, threading, rects):
    #Passing the TieUp as the Transpose
    pattern = np.matmul(tie_upT, threading)

    for i in range(np.shape(pattern)[0]):
        for j in range(np.shape(pattern)[1]):
            x = j * block_size + (j + 1) * buffer
            y = i * block_size + (i + 1) * buffer
            canvas.delete(text[i][j])
            canvas.delete((rects[i][j]))
            if pattern[i][j] == 1:
                text_color = product_0_color
                back_color = product_1_color
            else:
                text_color = product_1_color
                back_color = product_0_color
            rects[i][j] = canvas.create_rectangle(x, y, x + block_size, y + block_size, fill=back_color)
            text[i][j] = canvas.create_text(x + block_size / 2, y + block_size / 2, text=str(pattern[i][j]),
                                            fill=text_color, font='Helvetica 15')
    return pattern