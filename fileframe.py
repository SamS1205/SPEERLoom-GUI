try:
    import tkinter as tk  # python 3
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk  # python 2
    import tkFont as tkfont  # python 2
import numpy as np
from serialCom import move_row
import matplotlib.pyplot as plt
from skimage.color import rgb2gray

weave1_width = 1500
weave1_height = 800
block_size = 25
buffer = 1
color0 = "white"
color1 = "black"
color0_text = "black"
color1_text = "white"



class FileFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.geo = str(weave1_width) + "x" + str(weave1_height)
        self.pat_text = []
        self.pattern = []
        self.rows = 0
        self.cols = 0

        label = tk.Label(self, text="Jacquard Loom Weaving", font=controller.title_font)
        instr = tk.Label(self, text="Load your csv pattern file by typing the file path and pressing the \'Load File\'"
                                    "button. \nUse the buttons on the left to see your cloth properties and "
                                    "the buttons on the right to weave your pattern.", font='Helvetica 12')

        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        load_button = tk.Button(self, text="Load File", command=lambda: self.show_file())
        fall_apart_button = tk.Button(self, text="Single Cloth?",
                                      command=lambda: calc_integrity(self.pattern, self.rows, self.cols, self.num_cloths))
        weave_factor_button = tk.Button(self, text="Weave Factor?",
                                        command=lambda: calc_weave_factor(self.pattern, self.rows, self.cols, self.pat_canvas, self.m1, self.m2))

        #message = "G:\Shared drives\SHRED Lab\ActiveStudentsResearchFolders\SamSpeer_ResearchFolder\Projects\RoboLoom\Weaving Patterns\star_trek_pattern.csv"
        #H:\Shared drives\SHRED Lab\ActiveStudentsResearchFolders\SamSpeer_ResearchFolder\Projects\SpeerLoom\Weaving Patterns\large_loom_plain_weave.csv
        message = "your_path\your_file.csv"
        self.text_box = tk.Text(self,height=2,width=100,wrap='word'
        )
        self.text_box.insert('end', message)

        # Make a canvas for the pattern
        max_x = 41*block_size + 41*buffer
        pat_width = max_x
        pat_height = 800
        self.pat_canvas = tk.Canvas(self, bg='#FFFFFF', width=pat_width, height=pat_height, scrollregion=(0, 0, max_x, 80*block_size))
        hbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        hbar.config(command=self.pat_canvas.xview)
        vbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vbar.config(command=self.pat_canvas.yview)
        self.pat_canvas.config(width=pat_width, height=pat_height)
        self.pat_canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

        self.num_cloths = tk.Label(self, text="? cloths")
        self.m1 = tk.Label(self, text="M1 = ?")
        self.m2 = tk.Label(self, text="M2 = ?")

        self.highlight = None
        button_weave = tk.Button(self, text="Next row", command=lambda: self.weave_row(True))
        button_weave_back = tk.Button(self, text="Prev row", command=lambda: self.weave_row(False))
        self.pat_row = 0

        # Arrange everything in a grid
        label.grid(row=0, column=0, columnspan=3)
        instr.grid(row=1, column=0, columnspan=3)
        button.grid(row=2, column=0, columnspan=3)

        self.text_box.grid(row=3, column=1, columnspan=2)
        load_button.grid(row=3, column=0)

        hbar.grid(row=9, column=1, sticky=tk.EW)
        vbar.grid(row=4, column=2, sticky=tk.NS, rowspan=5)
        self.pat_canvas.grid(row=4, column=1, rowspan=5)

        fall_apart_button.grid(row=4, column=0)
        weave_factor_button.grid(row=6, column=0)
        self.num_cloths.grid(row=5, column=0)
        self.m1.grid(row=7, column=0)
        self.m2.grid(row=8, column=0)

        button_weave.grid(row=4, column=3)
        button_weave_back.grid(row=3, column=3)

    def show_file(self):
        file = self.text_box.get("1.0","end-1c")

        if ".csv" in file:
            self.pattern = np.genfromtxt(file, delimiter=',', dtype=int)
        else:
            img = plt.imread(file)[:,0:40,0:3]
            self.pattern = (rgb2gray(img)>0.5).astype(int)
        self.cols = len(self.pattern[0])
        self.rows = len(self.pattern)

        self.pat_canvas.delete("all")
        self.m1.config(text="M1 = ?")
        self.m2.config(text="M2 = ?")
        self.num_cloths.config(text="? cloths")

        text = []
        for row in range(self.rows):
            text_row = []
            for column in range(self.cols):
                x = column * block_size + (column + 1) * buffer +block_size+2*buffer
                y = row * block_size + (row + 1) * buffer + block_size+2*buffer
                color = color1
                color_text = color1_text
                if self.pattern[row,column] == 0:
                    color = color0
                    color_text = color0_text
                self.pat_canvas.create_rectangle(x, y, x + block_size, y + block_size, fill=color, outline="")
                text_row.append(self.pat_canvas.create_text(x + block_size / 2, y + block_size / 2,
                                                            text=str(self.pattern[row,column]), fill=color_text,
                                                   font=('Helvetica 15 bold')))
            text.append(text_row)
        self.pat_text = text
        self.pat_row = 0

    def weave_row(self, forward):
        if forward:
            self.pat_row += 1
        else:
            self.pat_row -= 1
        if self.pat_row > self.rows:
            self.pat_row = 1
        elif self.pat_row <= 0:
            self.pat_row = self.rows
        self.pat_canvas.delete(self.highlight)
        x0 = 2*buffer+block_size
        y0 = (self.pat_row-1) * (block_size + buffer)+2*buffer+block_size
        x1 = (self.cols+1) * ( block_size + buffer) + buffer / 2
        y1 = y0 + block_size + buffer/2
        self.highlight = self.pat_canvas.create_rectangle(x0, y0, x1, y1, width=buffer*2, outline="green")
        move_row(self.pattern[self.pat_row - 1])

def calc_weave_factor(pattern, rows, cols, pat_canvas, m1_label, m2_label):
    print("Weave Factor")
    if pattern == []:
        return
    horz_padded = np.append(pattern, np.reshape(pattern[:, 0], (rows, 1)), axis=1)
    horz_diff = np.absolute(np.diff(horz_padded, axis=1))

    vert_padded = np.append(pattern, np.reshape(pattern[0, :], (1, cols)), axis=0)
    vert_diff = np.absolute(np.diff(vert_padded, axis=0))

    # Sum
    horz_sum = np.sum(horz_diff)
    horz_sums_vec = np.sum(horz_diff, axis=1) / cols
    m1 = rows ** 2 / horz_sum
    print(m1)

    vert_sum = np.sum(vert_diff)
    vert_sums_vec = np.sum(vert_diff, axis=0)/rows
    m2 = cols ** 2 / vert_sum
    print(m2)

    m1_label.config(text="M1 = "+str(m1)[0:3])
    m2_label.config(text="M2 = " + str(m2)[0:3])

    for row in range(rows):
        y = row * block_size + (row + 1) * buffer
        y = y + block_size + 2*buffer
        r = str(hex(int(255)))[2:]
        g = str(hex(int((horz_sums_vec[row])*255)))[2:]
        b = str(hex(int((horz_sums_vec[row])*255)))[2:]
        if len(g) == 1:
            g = "0"+g
        if len(b) == 1:
            b = "0"+b
        color = "#" + r+g+b
        pat_canvas.create_rectangle(buffer, y, block_size + buffer, y + block_size, fill=color, outline="")
    for col in range(cols):
        x = col * block_size + (col + 1) * buffer
        x = x + block_size + 2 * buffer
        r = str(hex(int(255)))[2:]
        g = str(hex(int((vert_sums_vec[col]) * 255)))[2:]
        b = str(hex(int((vert_sums_vec[col]) * 255)))[2:]
        if len(g) == 1:
            g = "0"+g
        if len(b) == 1:
            b = "0"+b
        color = "#" + str(r+g+b)
        pat_canvas.create_rectangle(x, buffer, x + block_size, block_size + buffer, fill=color, outline="")

def calc_integrity(pattern, rows, cols, label):
    # Go through each combination of rows and columns to break them into sets and see if they'd fall apart
    fall_apart = False

    for c1 in range(cols):
        Ac = np.array([c1])

        # find the places in the Ac column that HAVE to be in Ar, i.e. where it's zero
        Ar = np.argwhere(pattern[:, Ac] == 0)[:, 0]
        if len(Ar) == 0:
            break

        # find the places in the Ar rows that are 1 indicating those cols HAVE to be Ac
        rows1 = np.unique(np.argwhere(pattern[Ar, :] == 1)[:, 1])
        Ac = np.concatenate((Ac, rows1))
        if len(Ac) == 0:
            break

        # Assume the rest are in B set and see if this breaks
        Br = [x for x in range(rows) if x not in Ar]
        Bc = [y for y in range(cols) if y not in Ac]

        # While there are elements of the B set, see if it falls apart, and if not, see if we can make it fall apart
        while len(Br) > 0 and len(Bc) > 0:
            # find AcxBr and BcxAr
            AcxBr = pattern[Br, :][:, Ac]
            BcxAr = pattern[Ar, :][:, Bc]
            if np.all(np.unique(AcxBr)) == 1 and np.all(np.unique(BcxAr) == 0):
                # cloth falls apart
                fall_apart = True
                break
            else:
                # Move rows containing 0 in AcxBr to Ar
                potential_new_Ar = np.unique(np.argwhere(pattern[:, Ac] == 0)[:, 0])
                new_Ar = np.array([ar for ar in potential_new_Ar if ar in Br])
                if len(new_Ar) > 0:
                    Ar = np.concatenate((Ar, new_Ar))

                # Move cols containing 1 in BcxAr to Ac
                potential_new_Ac = np.unique(np.argwhere(pattern[Ar, :] == 1)[:, 1])
                new_Ac = np.array([ac for ac in potential_new_Ac if ac in Bc])
                if len(new_Ac) > 0:
                    Ac = np.concatenate((Ac, new_Ac))

                # Make the new B sets
                Br = [x for x in range(rows) if x not in Ar]
                Bc = [y for y in range(cols) if y not in Ac]

        if fall_apart:
            break



    # Print the sets
    if fall_apart:
        print("Cloth will fall apart")
        print("A columns")
        print(Ac)
        print("A rows")
        print(Ar)
        print("B columns")
        print(Bc)
        print("B rows")
        print(Br)
        label.config(text="2 cloths")
    else:
        print("Cloth will not fall apart")
        label.config(text="1 cloth")