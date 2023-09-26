try:
    import tkinter as tk  # python 3
    from tkinter import ttk # python 3
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk  # python 2
    import tkFont as tkfont  # python 2
import numpy as np
from constants import *


class MathMode_Page1(tk.Frame):

    def __init__(self, parent, controller):
      tk.Frame.__init__(self, parent)
      self.controller = controller
      self.parent     = parent
      self.geo        = str(mathMode_width) + "x" + str(mathMode_height_2)

      self.rows    = 25
      self.columns = 20 

      #Create Labels & buttons
      label       = tk.Label(self, text="Mini Math Mode", font=controller.title_font)
      label_x     = tk.Label(self, text="X", font=controller.title_font)
      label_equal = tk.Label(self, text="=", font=controller.title_font)

      label_th    = tk.Label(self, text="Threading (Th)", font=controller.title_font)
      label_tu_T  = tk.Label(self, text="Tie-upᵀ (Tuᵀ)", font=controller.title_font)
      label_p     = tk.Label(self, text="Product (P)", font=controller.title_font)      

      button_back     = tk.Button(self, text="Back", command=lambda: [self.destroyPage(),
                                                                          controller.show_frame("MathMode_WelcomePage")])
      button_continue = tk.Button(self, text="Continue", command=lambda: [controller.get_page("MathMode_Page2").init_page(self.product_matrix),
                                                                          controller.show_frame("MathMode_Page2")])
      button_check    = tk.Button(self, text="Check Answer", command=lambda: self.check_answer())
      button_reset    = tk.Button(self, text="Reset Product Matrix", command=lambda: self.reset_product_canvas())

      self.pat_row   = 0
      self.highlight = None

      #Placing Objects
      label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)
      label_x.place(relx=0.4, rely=0.3, anchor=tk.W)
      label_equal.place(relx=0.65, rely=0.3, anchor=tk.W)
      
      label_th.place(relx=0.45, rely=0.2)
      label_tu_T.place(relx=0.1, rely=0.2)
      label_p.place(relx= 0.7, rely=0.2)
      
      button_back.place(relx=0.26, rely= 0.1)
      button_continue.place(relx=0.3, rely= 0.1)
      button_check.place(relx=0.6, rely= 0.1)
      button_reset.place(relx=0.7, rely= 0.1)
      
    
    def init_page(self):
      self.pattern = np.zeros((self.controller.num_pedals, NUM_MOTORS_DIS), dtype=int)
      
      self.make_tieupT_canvas()
      #self.make_tieup_canvas()
      self.make_threading_canvas()
      self.make_product_canvas()
      self.reset_product_canvas()

    def onHover(self, event):
      tieUp_num_rows, tieUp_num_cols = self.tie_upT.shape
      thread_num_rows, thread_num_cols = self.threading.shape

      c = int(event.x / (block_size + buffer))
      r = int(event.y / (block_size + buffer))

      x = c * block_size + (c + 1) * buffer
      y = r * block_size + (r + 1) * buffer

      self.tieupT_canvas.create_rectangle(0, y, (x + block_size)*tieUp_num_rows, (y + block_size), 
                                                               dash=(5,2), outline=highlight_color, tags="temporary", width=5)
      self.threading_canvas.create_rectangle(x, 0, (x + block_size), (y + block_size)*thread_num_cols, 
                                                               dash=(5,2), outline=highlight_color, tags="temporary", width=5)

    def onHoverLeave(self):
      self.threading_canvas.delete(self.threading_canvas.find_withtag("temporary"))
      self.tieupT_canvas.delete(self.tieupT_canvas.find_withtag("temporary"))

    def onMatClick(self, canvas, matrix, text, event, color0, color1, rects):
      col = int(event.x / (block_size + buffer))
      row = int(event.y / (block_size + buffer))
      if (event.x <= ((col + 1) * (block_size + buffer) - buffer)) and \
              (event.y <= ((row + 1) * (block_size + buffer) - buffer)):
          matrix[row][col] = not matrix[row][col]
      x = col * block_size + (col + 1) * buffer
      y = row * block_size + (row + 1) * buffer
      if matrix[row][col] == 1:
          text_color = color0
          back_color = color1
      else:
          text_color = color1
          back_color = color0
      canvas.delete(rects[row][col])
      rects[row][col] = canvas.create_rectangle(x, y, x + block_size, y + block_size, fill=back_color, tags="highlight")
      canvas.delete(text[row][col])
      text[row][col] = canvas.create_text(x + block_size / 2, y + block_size / 2, text=str(matrix[row][col]),
                                          fill=text_color, font='Helvetica 15', tags="highlight")
      
      self.threading_canvas.delete(self.threading_canvas.find_withtag("temporary"))
      self.tieupT_canvas.delete(self.tieupT_canvas.find_withtag("temporary"))
        
    def make_product_canvas(self):
      dynamic_y = (block_size + buffer) * self.controller.num_pedals

      self.product_canvas = tk.Canvas(self, height=dynamic_y, width=(block_size + buffer) * NUM_MOTORS_DIS + buffer)
      self.product_text, self.product_rects = populate_matrix(self.product_canvas, self.controller.num_pedals,
                                                              NUM_MOTORS_DIS, product_0_color, product_1_color)
      
      self.product_matrix = np.zeros((self.controller.num_pedals, NUM_MOTORS_DIS), dtype=int)
      self.product_canvas.bind('<Button-1>',
                                  lambda event, canvas=self.product_canvas, matrix=self.product_matrix,
                                        text=self.product_text, rects=self.product_rects:
                                  self.onMatClick(canvas, matrix, text, event, product_0_color,
                                                  product_1_color, rects))

      #Highlight Rows & Columns on Tie-up & Threading
      self.product_canvas.tag_bind("highlight", "<Enter>",
                                    lambda event: self.onHover(event))
      
      self.product_canvas.tag_bind("highlight", "<Leave>",
                                    lambda event: self.onHoverLeave())

      product_dim       = str(self.controller.num_pedals) + " x " + str(NUM_MOTORS_DIS) 
      label_product_dim = tk.Label(self, text=product_dim, font=self.controller.title_font) 
      
      self.product_canvas.place(relx=0.7, rely=0.3)
      label_product_dim.place(relx=0.7, y=dynamic_y+125)
    
    def make_threading_canvas(self):
      dynamic_y = (block_size + buffer) * self.controller.num_frames
      self.threading_canvas = tk.Canvas(self, height=(block_size + buffer) * self.controller.num_frames,
                                        width=(block_size + buffer) * NUM_MOTORS_DIS + buffer)
      self.threading_text, self.threading_rects = populate_matrix(self.threading_canvas, self.controller.num_frames,
                                                                  NUM_MOTORS_DIS, threading_0_color,
                                                                  threading_1_color)
      self.threading = np.zeros((self.controller.num_frames, NUM_MOTORS_DIS), dtype=int)
      self.threading_canvas.bind('<Button-1>',
                                  lambda event, canvas=self.threading_canvas, matrix=self.threading,
                                        text=self.threading_text, rects=self.threading_rects:
                                  self.onMatClick(canvas, matrix, text, event, threading_0_color,
                                                  threading_1_color, rects))
      
      threading_dim = str(self.controller.num_frames) + " x " + str(NUM_MOTORS_DIS)

      self.label_threading_dim = tk.Label(self, text=threading_dim, font=self.controller.title_font) 

      self.threading_canvas.place(relx=0.45, rely=0.3)
      self.label_threading_dim.place(relx=0.45, y=dynamic_y+125)

    def make_tieupT_canvas(self):
      dynamic_y = (block_size + buffer) * self.controller.num_pedals + buffer

      self.tieupT_canvas = tk.Canvas(self, height=dynamic_y, width=(block_size + buffer) * self.controller.num_frames)
      self.tie_upT_text, self.tie_upT_rects = populate_matrix(self.tieupT_canvas, self.controller.num_pedals,
                                                            self.controller.num_frames, tie_up_0_color,
                                                            tie_up_1_color)
      self.tie_upT = np.zeros((self.controller.num_pedals, self.controller.num_frames), dtype=int)
      self.tieupT_canvas.bind('<Button-1>',
                              lambda event, canvas=self.tieupT_canvas, matrix=self.tie_upT,
                                    text=self.tie_upT_text, rects=self.tie_upT_rects:
                              self.onMatClick(canvas, matrix, text, event, tie_up_0_color, tie_up_1_color, rects))
      tieupT_dim           = str(self.controller.num_pedals) + " x " + str(self.controller.num_frames) 
      self.label_tieupT_dim = tk.Label(self, text=tieupT_dim, font=self.controller.title_font) 

      self.tieupT_canvas.place(relx=0.1, rely=0.3)
      self.label_tieupT_dim.place(relx=0.1, y=dynamic_y+125)

    def make_tieup_canvas(self):
      dynamic_y = (block_size + buffer) * self.controller.num_frames

      self.tieup_canvas = tk.Canvas(self, height=dynamic_y, width=(block_size + buffer) * self.controller.num_pedals + buffer)
      self.tie_up_text, self.tie_up_rects = populate_matrix(self.tieup_canvas, self.controller.num_frames,
                                                            self.controller.num_pedals, pattern_0_color,
                                                            pattern_1_color)
      self.tie_up = np.zeros((self.controller.num_frames, self.controller.num_pedals), dtype=int)
      tieup_dim       = str(self.controller.num_frames) + " x " + str(self.controller.num_pedals)
      self.label_tieup_dim = tk.Label(self, text=tieup_dim, font=self.controller.title_font) 

      self.tieup_canvas.place(relx=0.1, rely=0.75)
      self.label_tieup_dim.place(relx=0.25, rely=0.75 + (dynamic_y/mathMode_height))

    def destroyPage(self):
      #self.tieup_canvas.destroy()
      self.tieupT_canvas.destroy()
      self.product_canvas.destroy()
      self.threading_canvas.destroy()
      self.label_threading_dim.destroy()
      #self.label_tieup_dim.destroy()
      self.label_tieupT_dim.destroy()
    
    def check_answer(self):
      self.pattern = np.matmul(self.tie_upT, self.threading)
      highlight_pattern(self.product_canvas, self.pattern, self.product_matrix, self.product_text, self.product_rects)
 
    def reset_product_canvas(self):
      self.product_canvas.destroy()
      self.make_product_canvas()


def populate_matrix(canvas, rows, cols, color_background, color_text):
    text = []
    rects = []
    for row in range(rows):
        text_row = []
        rects_row = []
        for column in range(cols):
            x = column * block_size + (column + 1) * buffer
            y = row * block_size + (row + 1) * buffer
            rects_row.append(canvas.create_rectangle(x, y, x + block_size, y + block_size, fill=color_background, tags="highlight"))
            text_row.append(canvas.create_text(x + block_size / 2, y + block_size / 2, text="0", fill=color_text,
                                               font=('Helvetica 15'), tags="highlight"))
        text.append(text_row)
        rects.append(rects_row)
    return text, rects

def highlight_pattern(canvas, pattern, product_matrix, text, rects):
    for i in range(np.shape(pattern)[0]):
        for j in range(np.shape(pattern)[1]):
            x = j * block_size + (j + 1) * buffer
            y = i * block_size + (i + 1) * buffer
            canvas.delete(text[i][j])
            canvas.delete((rects[i][j]))
            if product_matrix[i][j] == pattern[i][j]:
                text_color = green_0_color
                back_color = green_1_color
            else:
                text_color = red_0_color
                back_color = red_1_color
            rects[i][j] = canvas.create_rectangle(x, y, x + block_size, y + block_size, fill=back_color)
            text[i][j] = canvas.create_text(x + block_size / 2, y + block_size / 2, text=str(pattern[i][j]),
                                            fill=text_color, font='Helvetica 15')
    return pattern

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
