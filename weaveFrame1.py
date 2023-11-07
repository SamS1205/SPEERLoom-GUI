try:
    import tkinter as tk  # python 3
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk  # python 2
    import tkFont as tkfont  # python 2
import numpy as np
from serialCom import move_frame, init_frames

weave1_width = 1400
weave1_height = 1000
block_size = 30
buffer = 2

tie_up_0_color = "#022b75"
tie_up_1_color = "#80a2e0"

threading_0_color = "#3d026e"
threading_1_color = "#c1abde"

treadling_0_color = "#034a01"
treadling_1_color = "#98c997"

pattern_0_color = "white"
pattern_1_color = "black"

#SHAFT LOOM WEAVING
class WeaveFrame1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.geo = str(weave1_width) + "x" + str(weave1_height)

        # Make this changeable later?
        self.rows = 20

        label = tk.Label(self, text="Shaft Loom Weaving", font=controller.title_font)
        instr = tk.Label(self, text="Change the number of shafts and pedals for your shaft loom setup. "
                                    "Then change the matrices by clicking on the boxes. \nOnce your pattern is complete, "
                                    "weave using the \'Next Row\' and \'Previous Row\' buttons", font='Helvetica 12')
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button_weave = tk.Button(self, text="Next Row", command=lambda: self.weave_row(True))
        button_weave_back = tk.Button(self, text="Previous Row", command=lambda: self.weave_row(False))
        self.pat_row = 0
        self.highlight = None

        # make and populate the canvases
        # Make a canvas for the pattern
        self.pattern_canvas = tk.Canvas(self, height=(block_size + buffer) * self.rows,
                                        width=(block_size + buffer) * self.controller.num_motors + buffer)
        self.pattern_text, self.pattern_rects = populate_matrix(self.pattern_canvas, self.rows,
                                            self.controller.num_motors, pattern_0_color, pattern_1_color)
        self.pattern = np.zeros((self.rows, self.controller.num_motors), dtype=int)

        # Make a tie up matrix canvas
        self.make_threading_canvas()

        # Make a tieup canvas
        self.make_tieup_canvas()

        # Make a treadling canvas
        self.make_treadling_canvas()

        # make buttons for num frames and num pedals
        button_frames = tk.Button(self, text="Set # of Shafts", command=self.set_frames)
        button_pedals = tk.Button(self, text="Set # of Pedals", command=self.set_pedals)
        self.text_box_frames = tk.Text(self, height=1, width=2, wrap='word')
        self.text_box_frames.insert('end', self.controller.num_frames)
        self.text_box_pedals = tk.Text(self, height=1, width=2, wrap='word')
        self.text_box_pedals.insert('end', self.controller.num_pedals)

        # Position things in frame
        label.grid(row=0, column=1, columnspan=6)

        instr.grid(row=1, column=1, columnspan=6)

        button.grid(row=2, column=1, columnspan=6)

        button_frames.grid(row=3, column=1)
        button_pedals.grid(row=3, column=3)
        self.text_box_frames.grid(row=3, column=2)
        self.text_box_pedals.grid(row=3, column=4)

        self.threading_canvas.grid(row=4, column=1, columnspan=4)
        self.tieup_canvas.grid(row=4, column=6)
        self.pattern_canvas.grid(row=5, column=1, columnspan=4, rowspan=2)
        self.treadling_canvas.grid(row=5, column=6, rowspan=2)
        button_weave.grid(row=5, column=0)
        button_weave_back.grid(row=6, column=0)


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
        rects[row][col] = canvas.create_rectangle(x, y, x + block_size, y + block_size, fill=back_color)
        canvas.delete(text[row][col])
        text[row][col] = canvas.create_text(x + block_size / 2, y + block_size / 2, text=str(matrix[row][col]),
                                            fill=text_color, font='Helvetica 15')
        self.pattern = update_pattern(self.pattern_canvas, self.pattern_text, self.pattern, self.threading,
                                      self.tie_up, self.treadling, self.pattern_rects)

    def weave_row(self, forward):
        if forward:
            self.pat_row += 1
        else:
            self.pat_row -= 1
        if self.pat_row > self.rows:
            self.pat_row = 1
        elif self.pat_row <= 0:
            self.pat_row = self.rows
        self.pattern_canvas.delete(self.highlight)
        x0 = buffer
        y0 = (self.pat_row - 1) * (block_size + buffer) + buffer
        x1 = (self.controller.num_motors) * (block_size + buffer) + buffer / 2
        y1 = y0 + block_size + buffer / 2
        self.highlight = self.pattern_canvas.create_rectangle(x0, y0, x1, y1, width=buffer * 2, outline="green")
        # CHANGE THIS TO MOVE FRAME with the frame from treadling*tie up
        # Send a list of frames
        # Frames starts as a list of 0s. Where treadling is 1, get tieup column, or col with frames, send that

        #Find where treadling is 1
        pedals_pressed = np.where(self.treadling[self.pat_row - 1]==1)[0]
        print(pedals_pressed)
        frames = np.zeros((self.controller.num_frames), dtype='int')
        for pedal in pedals_pressed:
            print(pedal)
            print(frames)
            print(np.resize(self.tie_up[:, pedal], (self.controller.num_frames)))
            frames = np.bitwise_or(frames, self.tie_up[:, pedal])
            print(frames)

        move_frame(frames)

    def set_frames(self):
        self.controller.num_frames = int(self.text_box_frames.get("1.0", "end-1c"))

        init_frames(self.controller.num_frames)

        # resize the threading and tie_up canvas and return everything to zeros
        self.threading_canvas.delete("all")
        self.threading_canvas.config(width=(block_size + buffer) * self.controller.num_motors + buffer,
                                     height=(block_size + buffer) * self.controller.num_frames)
        self.threading_text, self.threading_rects = populate_matrix(self.threading_canvas, self.controller.num_frames,
                                                                    self.controller.num_motors, threading_0_color,
                                                                    threading_1_color)
        self.threading = np.zeros((self.controller.num_frames, self.controller.num_motors), dtype=int)

        #self.make_threading_canvas()
        #self.make_tieup_canvas()

        self.tieup_canvas.delete("all")
        self.tieup_canvas.config(height=(block_size + buffer) * self.controller.num_frames,
                                      width=(block_size + buffer) * self.controller.num_pedals + buffer)
        self.tie_up_text, self.tie_up_rects = populate_matrix(self.tieup_canvas, self.controller.num_frames,
                                                              self.controller.num_pedals, tie_up_0_color,
                                                              tie_up_1_color)
        self.tie_up = np.zeros((self.controller.num_frames, self.controller.num_pedals), dtype=int)

        #rebind buttons with new thing
        self.threading_canvas.bind('<Button-1>',
                                   lambda event, canvas=self.threading_canvas, matrix=self.threading,
                                          text=self.threading_text, rects=self.threading_rects:
                                   self.onMatClick(canvas, matrix, text, event, threading_0_color,
                                                   threading_1_color, rects))
        self.tieup_canvas.bind('<Button-1>',
                               lambda event, canvas=self.tieup_canvas, matrix=self.tie_up,
                                      text=self.tie_up_text, rects=self.tie_up_rects:
                               self.onMatClick(canvas, matrix, text, event, tie_up_0_color, tie_up_1_color, rects))


        print("FRAMES")

    def set_pedals(self):
        self.controller.num_pedals = int(self.text_box_pedals.get("1.0", "end-1c"))
        # remake the tie_up and treadling canvas

        self.tieup_canvas.delete("all")
        self.tieup_canvas.config(height=(block_size + buffer) * self.controller.num_frames,
                                 width=(block_size + buffer) * self.controller.num_pedals + buffer)
        self.tie_up_text, self.tie_up_rects = populate_matrix(self.tieup_canvas, self.controller.num_frames,
                                                              self.controller.num_pedals, tie_up_0_color,
                                                              tie_up_1_color)
        self.tie_up = np.zeros((self.controller.num_frames, self.controller.num_pedals), dtype=int)


        self.treadling_canvas.delete("all")
        self.treadling_canvas.config(height=(block_size + buffer) * self.rows,
                                          width=(block_size + buffer) * self.controller.num_pedals + buffer)
        self.treadling_text, self.treadling_rects = populate_matrix(self.treadling_canvas, self.rows,
                                                                    self.controller.num_pedals, treadling_0_color,
                                                                    treadling_1_color)
        self.treadling = np.zeros((self.rows, self.controller.num_pedals), dtype=int)

        # rebind buttons with new thing
        self.tieup_canvas.bind('<Button-1>',
                               lambda event, canvas=self.tieup_canvas, matrix=self.tie_up,
                                      text=self.tie_up_text, rects=self.tie_up_rects:
                               self.onMatClick(canvas, matrix, text, event, tie_up_0_color, tie_up_1_color, rects))
        self.treadling_canvas.bind('<Button-1>',
                                   lambda event, canvas=self.treadling_canvas, matrix=self.treadling,
                                          text=self.treadling_text, rects=self.treadling_rects:
                                   self.onMatClick(canvas, matrix, text, event, treadling_0_color,
                                                   treadling_1_color, rects))
        print("PEDALS")

    def make_threading_canvas(self):
        self.threading_canvas = tk.Canvas(self, height=(block_size + buffer) * self.controller.num_frames,
                                          width=(block_size + buffer) * self.controller.num_motors + buffer)
        self.threading_text, self.threading_rects = populate_matrix(self.threading_canvas, self.controller.num_frames,
                                                                    self.controller.num_motors, threading_0_color,
                                                                    threading_1_color)
        self.threading = np.zeros((self.controller.num_frames, self.controller.num_motors), dtype=int)
        self.threading_canvas.bind('<Button-1>',
                                   lambda event, canvas=self.threading_canvas, matrix=self.threading,
                                          text=self.threading_text, rects=self.threading_rects:
                                   self.onMatClick(canvas, matrix, text, event, threading_0_color,
                                                   threading_1_color, rects))

    def make_tieup_canvas(self):
        self.tieup_canvas = tk.Canvas(self, height=(block_size + buffer) * self.controller.num_frames,
                                      width=(block_size + buffer) * self.controller.num_pedals + buffer)
        self.tie_up_text, self.tie_up_rects = populate_matrix(self.tieup_canvas, self.controller.num_frames,
                                                              self.controller.num_pedals, tie_up_0_color,
                                                              tie_up_1_color)
        self.tie_up = np.zeros((self.controller.num_frames, self.controller.num_pedals), dtype=int)
        self.tieup_canvas.bind('<Button-1>',
                               lambda event, canvas=self.tieup_canvas, matrix=self.tie_up,
                                      text=self.tie_up_text, rects=self.tie_up_rects:
                               self.onMatClick(canvas, matrix, text, event, tie_up_0_color, tie_up_1_color, rects))

    def make_treadling_canvas(self):
        self.treadling_canvas = tk.Canvas(self, height=(block_size + buffer) * self.rows,
                                          width=(block_size + buffer) * self.controller.num_pedals + buffer)
        self.treadling_text, self.treadling_rects = populate_matrix(self.treadling_canvas, self.rows,
                                                                    self.controller.num_pedals, treadling_0_color,
                                                                    treadling_1_color)
        self.treadling = np.zeros((self.rows, self.controller.num_pedals), dtype=int)
        self.treadling_canvas.bind('<Button-1>',
                                   lambda event, canvas=self.treadling_canvas, matrix=self.treadling,
                                          text=self.treadling_text, rects=self.treadling_rects:
                                   self.onMatClick(canvas, matrix, text, event, treadling_0_color,
                                                   treadling_1_color, rects))


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
                                               font=('Helvetica 15')))
        text.append(text_row)
        rects.append(rects_row)
    return text, rects


def update_pattern(canvas, text, pattern, threading, tie_up, treadling, rects):
    a = np.matmul(treadling, np.transpose(tie_up))
    pattern = np.matmul(a, threading)

    for i in range(np.shape(pattern)[0]):
        for j in range(np.shape(pattern)[1]):
            x = j * block_size + (j + 1) * buffer
            y = i * block_size + (i + 1) * buffer
            canvas.delete(text[i][j])
            canvas.delete((rects[i][j]))
            if pattern[i][j] == 1:
                text_color = pattern_0_color
                back_color = pattern_1_color
            else:
                text_color = pattern_1_color
                back_color = pattern_0_color
            rects[i][j] = canvas.create_rectangle(x, y, x + block_size, y + block_size, fill=back_color)
            text[i][j] = canvas.create_text(x + block_size / 2, y + block_size / 2, text=str(pattern[i][j]),
                                            fill=text_color, font='Helvetica 15')
    return pattern