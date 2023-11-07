try:
    import tkinter as tk  # python 3
    from tkinter import ttk  # python 3
    from tkinter import font as tkfont  # python 3
    from PIL import ImageTk, Image
except ImportError:
    import Tkinter as tk  # python 2
    import tkFont as tkfont  # python 2
import numpy as np
from constants import *
from constants_info import *
from ScrollableFrame import ScrollableFrame
from serialCom import move_frame, init_frames, config_frames

instr_message = "Welcome! To start, change the number of shafts and pedals for your shaft loom setup."
instr_message_2 = "Next, change the threading matrix to the desired configuration, pressing the"
instr_message_3 = "\'Transmit New Threading\' button when complete. Finally, click around the other matracies"
instr_message_4 = "until your desired pattern is complete! Weave using the \'Next Row\' and \'Previous Row\' buttons."
instr_message_5 = "To start exploring the mathematics behind weaving, press the \'Enter Math Mode\' button!"
instr_message_6 = "If you are struggling with any aspect of the weaving process, please consult the Side Navigation Menu to"
instr_message_7 = "explore common weaving terminology, a weaving draft legend, or review linear algebra concepts!"
instr_message_8 = "Additonally, the Side Navigation Menu has simple patterns and culturally significant woven structures to easily follow."


# TODO: Intential in design decisions: verbal, mathametical, and visual
class WeaveFrame1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.geo = str(weave1_width) + "x" + str(weave1_height)

        # TODO: Adjust Rows Dynamically, not locked to display all 25
        self.rows = 25
        self.columns = 20
        self.side_nav_state = False

        # Defining the Set X for Tie-Up & Treadling
        dynamic_x = (block_size + buffer) * self.controller.num_motors + buffer

        # Create Title
        label = tk.Label(self, text="Shaft Loom Weaving", font=controller.title_font)
        # Adding Console
        self.make_console(dynamic_x)

        # Create Buttons
        button_weave = tk.Button(self, text="Next Row", command=lambda: self.weave_row(True))
        button_weave_back = tk.Button(self, text="Previous Row", command=lambda: self.weave_row(False))
        side_nav_button = tk.Button(self, text="Toggle Side Menu", command=lambda: toggle_side_nav(self))
        button_sendConfig = tk.Button(self, text="Transmit New Threading",
                                      command=lambda: config_frames(self.threading))
        math_mode_button = tk.Button(self, text="Enter Math Mode",
                                     command=lambda: [controller.show_frame("MathMode_WelcomePage")])

        # Adding Side Navigation Panel
        self.make_side_nav_menu()

        self.pat_row = 0
        self.highlight = None

        # make and populate the canvases
        # Make a canvas for the pattern
        self.pattern_canvas = tk.Canvas(self, height=(block_size + buffer) * self.rows,
                                        width=(block_size + buffer) * self.controller.num_motors + buffer)
        self.pattern_text, self.pattern_rects = populate_matrix(self.pattern_canvas, self.rows,
                                                                self.controller.num_motors, pattern_0_color,
                                                                pattern_1_color)
        self.pattern = np.zeros((self.rows, self.controller.num_motors), dtype=int)

        # Make Menu bar
        self.make_menuBar()

        # Make a threading matrix canvas
        self.make_threading_canvas()

        # Make a tieup canvas
        self.make_tieup_canvas()

        # Make a treadling canvas
        self.make_treadling_canvas()

        # make buttons for num frames and num pedals
        self.make_pedal_frame_buttons()

        # Placing Objects
        label.place(relx=0.4, rely=0.01, anchor=tk.CENTER)

        self.button_frames.place(x=150, rely=0.15, anchor=tk.N)
        self.text_box_frames.place(x=210, rely=0.15, anchor=tk.N)
        self.button_pedals.place(x=dynamic_x + 100, rely=0.15)
        self.text_box_pedals.place(x=dynamic_x + 200, rely=0.15)
        side_nav_button.place(relx=0.17, rely=0.15)
        button_weave.place(relx=0.25, rely=0.15)
        button_weave_back.place(relx=0.3, rely=0.15)
        math_mode_button.place(relx=0.36, rely=0.15)
        button_sendConfig.place(relx=0.435, rely=0.15)

        self.threading_canvas.place(relx=0.05, rely=0.20)
        self.tieup_canvas.place(x=dynamic_x + 100, rely=0.20)
        self.pattern_canvas.place(relx=0.05, rely=0.3)
        self.treadling_canvas.place(x=dynamic_x + 100, rely=0.3)

        # Place Side Nav
        self.side_nav_frame.place(relx=1, rely=0.02, anchor=tk.NE)
        self.notebook.place(relx=0.5, rely=0, anchor=tk.N)

        # Display Console
        self.console_frame.place(relx=0.05, rely=0.03, anchor=tk.NW)
        self.console_text.pack(side=tk.LEFT)

    def make_console(self, dynamic_x):
        self.console_frame = tk.LabelFrame(self, height=console_height, width=dynamic_x + 140,
                                           bg=console_color, text="Console Log", relief=tk.RAISED)
        self.console_frame.pack_propagate(False)
        self.console_text = tk.Listbox(self.console_frame, height=console_height,
                                       width=dynamic_x + 140, selectmode=tk.SINGLE, font='Terminal 11')
        self.console_text.yview(True)
        self.console_text.insert(tk.END, instr_message)
        self.console_text.insert(tk.END, instr_message_2)
        self.console_text.insert(tk.END, instr_message_3)
        self.console_text.insert(tk.END, instr_message_4)
        self.console_text.insert(tk.END, instr_message_5)
        self.console_text.insert(tk.END, instr_message_6)
        self.console_text.insert(tk.END, instr_message_7)
        self.console_text.insert(tk.END, instr_message_8)
        self.console_text.itemconfig(self.console_text.size() - 8, bg='light green')
        self.console_text.itemconfig(self.console_text.size() - 7, bg='light green')
        self.console_text.itemconfig(self.console_text.size() - 6, bg='light green')
        self.console_text.itemconfig(self.console_text.size() - 5, bg='light green')
        self.console_text.itemconfig(self.console_text.size() - 4, bg='orange')
        self.console_text.itemconfig(self.console_text.size() - 3, bg='light blue')
        self.console_text.itemconfig(self.console_text.size() - 2, bg='light blue')
        self.console_text.itemconfig(self.console_text.size() - 1, bg='light blue')

    def make_menuBar(self):
        self.menu_bar = tk.Menu(self, tearoff=0, background="#d2d7d3")
        self.file_menu = tk.Menu(self.menu_bar, background="#d2d7d3")
        self.file_menu.add_command(label="Return Home", command=lambda: self.controller.show_frame("StartPage"))
        self.file_menu.add_command(label="Return to Education Mode",
                                   command=lambda: self.controller.show_frame("WeaveFrame1"))
        self.file_menu.add_command(label="Return to Free Weave Mode",
                                   command=lambda: self.controller.show_frame("FileFrame"))
        self.file_menu.add_command(label="Return to Calibrate Mode",
                                   command=lambda: self.controller.show_frame("CalFrame"))
        self.file_menu.add_command(label="Reset SPEERLoom", command=lambda: self.controller.show_frame("ResetFrame"))
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.controller.config(menu=self.menu_bar)

    def make_side_nav_menu(self):
        side_nav_height = weave1_height * .8
        side_nav_width_x = 775

        # TODO: Show Side Nav Menu on Top of Weaving Draft
        self.side_nav_frame = tk.Frame(self, width=75, height=weave1_height * .85,
                                       background=console_color, relief=tk.GROOVE, borderwidth=5)

        # Adding Notebook for Side Nav
        self.notebook = ttk.Notebook(self.side_nav_frame)
        self.weave_term = tk.Frame(self.notebook, bg=label_color, width=side_nav_width_x, height=side_nav_height)
        # self.weave_term.pack_propagate(False)
        self.weave_draft = tk.Frame(self.notebook, width=side_nav_width, height=side_nav_height)
        self.cult_patterns = tk.Frame(self.notebook, width=side_nav_width, height=side_nav_height)
        self.linear_alg = tk.Frame(self.notebook, width=side_nav_width, height=side_nav_height)

        self.populate_side_nav()

    def populate_side_nav(self):
        self.populate_weaving_term()
        self.populate_weaving_draft()
        self.populate_cultural_patterns()
        self.populate_linear_review()

    def populate_linear_review(self):
        # Opening All Images w/ Frames
        self.linear_im1 = ImageTk.PhotoImage(Image.open("weaving\\vector_example.png"))
        self.linear_im2 = ImageTk.PhotoImage(Image.open("weaving\\vector_addition.png"))
        self.linear_im3 = ImageTk.PhotoImage(Image.open("weaving\\vector_scalar.png"))
        self.linear_im4 = ImageTk.PhotoImage(Image.open("weaving\cloth_with_matrix.png"))
        self.linear_im5 = ImageTk.PhotoImage(Image.open("weaving\matrix_mult.png"))

        # Create Scrollable Frame
        self.cult_patterns.update_idletasks()
        self.linearRew_scroll_frame = ScrollableFrame(self.linear_alg)
        self.linearRew_scroll_frame.canvas.config(height=weave1_height * .8, width=side_nav_width)
        self.linearRew_scroll_frame.pack()

        # Labels for Text
        self.linR1 = tk.Label(self.linearRew_scroll_frame.scrollable_frame, text="Linear Algebra Review",
                              font='Helvetica 14 bold underline').pack()
        self.linR2 = tk.Label(self.linearRew_scroll_frame.scrollable_frame, text=linAlg_info,
                              font='Helvetica 10').pack()
        self.linR3 = tk.Label(self.linearRew_scroll_frame.scrollable_frame, text="____________",
                              font='Helvetica 11').pack()
        self.linR4 = tk.Label(self.linearRew_scroll_frame.scrollable_frame, text="Vectors",
                              font='Helvetica 12 bold').pack()
        self.linearIm1 = tk.Label(self.linearRew_scroll_frame.scrollable_frame, image=self.linear_im1, height=135,
                                  width=95).pack()
        self.linR5 = tk.Label(self.linearRew_scroll_frame.scrollable_frame, text=vector_def, font='Helvetica 11').pack()
        self.linR6 = tk.Label(self.linearRew_scroll_frame.scrollable_frame, text="Vector Operations",
                              font='Helvetica 12 bold').pack()
        self.linearIm2 = tk.Label(self.linearRew_scroll_frame.scrollable_frame, image=self.linear_im2, height=133,
                                  width=460).pack()
        self.linR7 = tk.Label(self.linearRew_scroll_frame.scrollable_frame, text=vector_ops_add,
                              font='Helvetica 11').pack()
        self.linearIm3 = tk.Label(self.linearRew_scroll_frame.scrollable_frame, image=self.linear_im3, height=114,
                                  width=100).pack()
        self.linR8 = tk.Label(self.linearRew_scroll_frame.scrollable_frame, text=vector_ops_scalar,
                              font='Helvetica 11').pack()
        self.linR9 = tk.Label(self.linearRew_scroll_frame.scrollable_frame, text="Matrix",
                              font='Helvetica 12 bold').pack()
        self.linR10 = tk.Label(self.linearRew_scroll_frame.scrollable_frame, text=matrix_def,
                               font='Helvetica 11').pack()
        self.linR10 = tk.Label(self.linearRew_scroll_frame.scrollable_frame, text="Woven Cloth as a Matrix Example",
                               font='Helvetica 11 underline').pack()
        self.linearIm4 = tk.Label(self.linearRew_scroll_frame.scrollable_frame, image=self.linear_im4, height=370,
                                  width=765).pack()
        self.linR11 = tk.Label(self.linearRew_scroll_frame.scrollable_frame, text="\nMatrix Operations",
                               font='Helvetica 12 bold').pack()
        self.linR12 = tk.Label(self.linearRew_scroll_frame.scrollable_frame, text=matrix_ops,
                               font='Helvetica 11').pack()
        self.linearIm5 = tk.Label(self.linearRew_scroll_frame.scrollable_frame, image=self.linear_im5, height=285,
                                  width=425).pack()

    def populate_cultural_patterns(self):
        # Opening All Images w/ Frames
        self.ct_im1 = ImageTk.PhotoImage(Image.open("weaving\plain_weave.png"))
        self.ct_im2 = ImageTk.PhotoImage(Image.open("weaving\\twill_weave.png"))
        self.ct_im3 = ImageTk.PhotoImage(Image.open("weaving\satin_weave.png"))
        self.ct_im4 = ImageTk.PhotoImage(Image.open("weaving\kente_cloth.png"))
        self.ct_im5 = ImageTk.PhotoImage(Image.open("weaving\kente_cloth_single_square.png"))
        self.ct_im6 = ImageTk.PhotoImage(Image.open("weaving\kente_drawdown.png"))
        self.ct_im7 = ImageTk.PhotoImage(Image.open("weaving\mayan_huipil.png"))
        self.ct_im8 = ImageTk.PhotoImage(Image.open("weaving\huipil_drawdown.png"))
        self.ct_im9 = ImageTk.PhotoImage(Image.open("weaving\mayan_huipil_patch.jpg"))

        # Create Scrollable Frame
        self.cult_patterns.update_idletasks()
        self.cp_scroll_frame = ScrollableFrame(self.cult_patterns)
        self.cp_scroll_frame.canvas.config(height=weave1_height * .8, width=side_nav_width)
        self.cp_scroll_frame.pack()

        # Labels for Text
        self.cp1 = tk.Label(self.cp_scroll_frame.scrollable_frame, text="Simple Patterns",
                            font='Helvetica 14 bold underline').pack()
        self.cp2 = tk.Label(self.cp_scroll_frame.scrollable_frame, text=cp_info, font='Helvetica 10').pack()
        self.cp3 = tk.Label(self.cp_scroll_frame.scrollable_frame, text="____________", font='Helvetica 11').pack()
        self.cp4 = tk.Label(self.cp_scroll_frame.scrollable_frame, text="Plain Weave", font='Helvetica 12 bold').pack()
        self.cp_twIm1 = tk.Label(self.cp_scroll_frame.scrollable_frame, image=self.ct_im1, height=178, width=178).pack()
        self.cp5 = tk.Label(self.cp_scroll_frame.scrollable_frame, text=plain_weave_def, font='Helvetica 11').pack()
        self.cp6 = tk.Label(self.cp_scroll_frame.scrollable_frame, text="Twill Weave", font='Helvetica 12 bold').pack()
        self.cp_twIm2 = tk.Label(self.cp_scroll_frame.scrollable_frame, image=self.ct_im2, height=178, width=178).pack()
        self.cp7 = tk.Label(self.cp_scroll_frame.scrollable_frame, text=twill_weave_def, font='Helvetica 11').pack()
        self.cp8 = tk.Label(self.cp_scroll_frame.scrollable_frame, text="Satin Weave", font='Helvetica 12 bold').pack()
        self.cp_twIm3 = tk.Label(self.cp_scroll_frame.scrollable_frame, image=self.ct_im3, height=178, width=178).pack()
        self.cp9 = tk.Label(self.cp_scroll_frame.scrollable_frame, text=satin_weave_def, font='Helvetica 11').pack()
        self.cp10 = tk.Label(self.cp_scroll_frame.scrollable_frame, text="Satin Weave Cultural Background",
                             font='Helvetica 11 italic bold').pack()
        self.cp11 = tk.Label(self.cp_scroll_frame.scrollable_frame, text=satin_weave_cul, font='Helvetica 11').pack()
        self.cp12 = tk.Label(self.cp_scroll_frame.scrollable_frame, text="Kente Cloth",
                             font='Helvetica 12 bold underline').pack()
        self.cp_twIm4 = tk.Label(self.cp_scroll_frame.scrollable_frame, image=self.ct_im4, height=420, width=750).pack()
        self.cp13 = tk.Label(self.cp_scroll_frame.scrollable_frame, text=kente_def, font='Helvetica 11').pack()
        self.cp_twIm5 = tk.Label(self.cp_scroll_frame.scrollable_frame, image=self.ct_im5, height=230, width=350).pack()
        self.cp14 = tk.Label(self.cp_scroll_frame.scrollable_frame, text=kente_instruct,
                             font='Helvetica 11 italic').pack()
        self.cp_twIm6 = tk.Label(self.cp_scroll_frame.scrollable_frame, image=self.ct_im6, height=455, width=750).pack()
        self.cp15 = tk.Label(self.cp_scroll_frame.scrollable_frame, text="Kente Cloth Cultural Background",
                             font='Helvetica 11 italic bold').pack()
        self.cp16 = tk.Label(self.cp_scroll_frame.scrollable_frame, text=kente_cult, font='Helvetica 11').pack()
        self.cp17 = tk.Label(self.cp_scroll_frame.scrollable_frame, text=kente_cult_2,
                             font='Helvetica 11 italic').pack()

        self.cp18 = tk.Label(self.cp_scroll_frame.scrollable_frame, text="Mayan Huipil",
                             font='Helvetica 12 bold underline').pack()
        self.cp_twIm7 = tk.Label(self.cp_scroll_frame.scrollable_frame, image=self.ct_im7, height=613, width=750).pack()
        self.cp19 = tk.Label(self.cp_scroll_frame.scrollable_frame, text=mayan_def, font='Helvetica 11').pack()
        self.cp_twIm9 = tk.Label(self.cp_scroll_frame.scrollable_frame, image=self.ct_im9, height=225, width=365).pack()
        self.cp19 = tk.Label(self.cp_scroll_frame.scrollable_frame, text=mayan_instruct,
                             font='Helvetica 11 italic').pack()
        self.cp_twIm8 = tk.Label(self.cp_scroll_frame.scrollable_frame, image=self.ct_im8, height=528, width=750).pack()
        self.cp20 = tk.Label(self.cp_scroll_frame.scrollable_frame, text="Huipil Cloth Cultural Background",
                             font='Helvetica 11 italic bold').pack()
        self.cp21 = tk.Label(self.cp_scroll_frame.scrollable_frame, text=mayan_cult, font='Helvetica 11').pack()
        self.cp22 = tk.Label(self.cp_scroll_frame.scrollable_frame, text=mayan_cult_2,
                             font='Helvetica 11 italic').pack()

    def populate_weaving_draft(self):
        # Opening All Images
        self.wd_im1 = ImageTk.PhotoImage(Image.open("weaving\weaving_draft_breakdown_labeled.png"))

        # Create Scrollable Frame
        self.weave_draft.update_idletasks()
        self.wd_scroll_frame = ScrollableFrame(self.weave_draft)
        self.wd_scroll_frame.canvas.config(height=weave1_height * .8, width=side_nav_width)
        self.wd_scroll_frame.pack()

        self.wd1 = tk.Label(self.wd_scroll_frame.scrollable_frame, text="Overview",
                            font='Helvetica 14 bold underline').pack()
        self.wd1_im = tk.Label(self.wd_scroll_frame.scrollable_frame, image=self.wd_im1, height=760, width=750).pack()
        self.wd2 = tk.Label(self.wd_scroll_frame.scrollable_frame, text="n= number of columns",
                            font='Helvetica 11').pack()
        self.wd3 = tk.Label(self.wd_scroll_frame.scrollable_frame, text="f= number of frames (shafts)",
                            font='Helvetica 11').pack()
        self.wd4 = tk.Label(self.wd_scroll_frame.scrollable_frame, text="p= number of pedals",
                            font='Helvetica 11').pack()
        self.wd5 = tk.Label(self.wd_scroll_frame.scrollable_frame, text="T= number of timesteps",
                            font='Helvetica 11').pack()

        self.wd6 = tk.Label(self.wd_scroll_frame.scrollable_frame, text="____________", font='Helvetica 11').pack()
        self.wd7 = tk.Label(self.wd_scroll_frame.scrollable_frame, text="Threading", font='Helvetica 12 bold').pack()
        self.wd8 = tk.Label(self.wd_scroll_frame.scrollable_frame, text=threading_def, font='Helvetica 11').pack()
        self.wd9 = tk.Label(self.wd_scroll_frame.scrollable_frame, text="Tie-Up", font='Helvetica 12 bold').pack()
        self.wd10 = tk.Label(self.wd_scroll_frame.scrollable_frame, text=tie_up_def, font='Helvetica 11').pack()
        self.wd11 = tk.Label(self.wd_scroll_frame.scrollable_frame, text="Treadling", font='Helvetica 12 bold').pack()
        self.wd12 = tk.Label(self.wd_scroll_frame.scrollable_frame, text=treadling_def, font='Helvetica 11').pack()
        self.wd13 = tk.Label(self.wd_scroll_frame.scrollable_frame, text="Drawdown", font='Helvetica 12 bold').pack()
        self.wd14 = tk.Label(self.wd_scroll_frame.scrollable_frame, text=drawdown_def, font='Helvetica 11').pack()

    def populate_weaving_term(self):
        # Opening All Images w/ Frames
        self.wt_im1 = ImageTk.PhotoImage(Image.open("weaving\heddles_on_shaft.png"))
        self.wt_im2 = ImageTk.PhotoImage(Image.open("weaving\speerloom.jpg"))

        # Create Scrollable Frame
        self.weave_draft.update_idletasks()
        self.wt_scroll_frame = ScrollableFrame(self.weave_term)
        self.wt_scroll_frame.canvas.config(height=weave1_height * .8, width=side_nav_width)
        self.wt_scroll_frame.pack()

        # TkLabel
        self.wt1 = tk.Label(self.wt_scroll_frame.scrollable_frame, text="Terminology",
                            font='Helvetica 14 bold underline').pack()
        self.wt2 = tk.Label(self.wt_scroll_frame.scrollable_frame, text="Wrap Threads", font='Helvetica 12 bold').pack()
        self.wt3 = tk.Label(self.wt_scroll_frame.scrollable_frame, text=warp_def, font='Helvetica 11').pack()
        self.wt4 = tk.Label(self.wt_scroll_frame.scrollable_frame, text="Weft Threads", font='Helvetica 12 bold').pack()
        self.wt5 = tk.Label(self.wt_scroll_frame.scrollable_frame, text=weft_def, font='Helvetica 11').pack()
        self.wt6 = tk.Label(self.wt_scroll_frame.scrollable_frame, text="Heddles", font='Helvetica 12 bold').pack()
        self.wt7 = tk.Label(self.wt_scroll_frame.scrollable_frame, text=heddle_def, font='Helvetica 11').pack()
        self.wt8 = tk.Label(self.wt_scroll_frame.scrollable_frame, text="Shafts (Frame)",
                            font='Helvetica 12 bold').pack()
        self.wt9 = tk.Label(self.wt_scroll_frame.scrollable_frame, text=shaft_def, font='Helvetica 11').pack()
        self.wt10 = tk.Label(self.wt_scroll_frame.scrollable_frame, text="Shed", font='Helvetica 12 bold').pack()
        self.wt11 = tk.Label(self.wt_scroll_frame.scrollable_frame, text=shed_def, font='Helvetica 11').pack()
        self.wt12 = tk.Label(self.wt_scroll_frame.scrollable_frame, text="Shuttle", font='Helvetica 12 bold').pack()
        self.wt13 = tk.Label(self.wt_scroll_frame.scrollable_frame, text=shuttle_def, font='Helvetica 11').pack()
        self.wt14 = tk.Label(self.wt_scroll_frame.scrollable_frame, text="Floats", font='Helvetica 12 bold').pack()
        self.wt15 = tk.Label(self.wt_scroll_frame.scrollable_frame, text=float_def, font='Helvetica 11').pack()

        self.wta = tk.Label(self.wt_scroll_frame.scrollable_frame, text="Types of Weaves",
                            font='Helvetica 12 bold underline').pack()
        self.wtb = tk.Label(self.wt_scroll_frame.scrollable_frame, text="Weft-Faced Weaving",
                            font='Helvetica 11 bold').pack()
        self.wtc = tk.Label(self.wt_scroll_frame.scrollable_frame, text=weft_face_def, font='Helvetica 11').pack()
        self.wtd = tk.Label(self.wt_scroll_frame.scrollable_frame, text="Warp-Faced Weaving",
                            font='Helvetica 11 bold').pack()
        self.wte = tk.Label(self.wt_scroll_frame.scrollable_frame, text=warp_face_def, font='Helvetica 11').pack()
        self.wtf = tk.Label(self.wt_scroll_frame.scrollable_frame, text="Balanced Weave",
                            font='Helvetica 11 bold').pack()
        self.wtg = tk.Label(self.wt_scroll_frame.scrollable_frame, text=balance_weave_def, font='Helvetica 11').pack()

        self.wt16 = tk.Label(self.wt_scroll_frame.scrollable_frame, text="\n\nShaft Loom Diagram",
                             font='Helvetica 12 bold underline').pack()
        self.wt1_im = tk.Label(self.wt_scroll_frame.scrollable_frame, image=self.wt_im1, height=750, width=490).pack()
        self.wt17 = tk.Label(self.wt_scroll_frame.scrollable_frame, text="\n\nSPEERLoom Diagram",
                             font='Helvetica 12 bold underline').pack()
        self.wt2_im = tk.Label(self.wt_scroll_frame.scrollable_frame, image=self.wt_im2, height=350, width=750).pack()

    def make_pedal_frame_buttons(self):
        self.button_frames = tk.Button(self, text="# of Shafts =", command=self.set_frames)
        self.button_pedals = tk.Button(self, text="# of Pedals =", command=self.set_pedals)
        self.text_box_frames = tk.Text(self, height=1, width=2, wrap='word')
        self.text_box_frames.insert('end', self.controller.num_frames)
        self.text_box_pedals = tk.Text(self, height=1, width=2, wrap='word')
        self.text_box_pedals.insert('end', self.controller.num_pedals)

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

        # Find where treadling is 1
        pedals_pressed = np.where(self.treadling[self.pat_row - 1] == 1)[0]
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
        oldHeight = (block_size + buffer) * self.controller.num_frames

        # Check Max/Min Frames Check
        input_frames = int(self.text_box_frames.get("1.0", "end-1c"))
        if input_frames < MIN_FRAMES:
            msg = "ERROR: Be careful, the SPEERLoom only supports a minimum of " + str(MIN_FRAMES) + " frames."
            self.console_text.insert(tk.END, msg)
            self.console_text.itemconfig(self.console_text.size() - 1, foreground='red')
            self.console_text.itemconfig(self.console_text.size() - 1, bg='pink')
            return
        elif input_frames > MAX_FRAMES:
            msg = "ERROR: Be careful, the SPEERLoom only supports a maximum of " + str(MAX_FRAMES) + " frames."
            self.console_text.insert(tk.END, msg)
            self.console_text.itemconfig(self.console_text.size() - 1, foreground='red')
            self.console_text.itemconfig(self.console_text.size() - 1, bg='pink')
            return
        else:
            self.controller.num_frames = input_frames
            init_frames(self.controller.num_frames)

        newHeight = (block_size + buffer) * self.controller.num_frames

        # resize the threading, return everything to zeros
        self.threading_canvas.delete("all")
        self.threading_canvas.config(width=(block_size + buffer) * self.controller.num_motors + buffer,
                                     height=(block_size + buffer) * self.controller.num_frames)
        self.threading_text, self.threading_rects = populate_matrix(self.threading_canvas, self.controller.num_frames,
                                                                    self.controller.num_motors, threading_0_color,
                                                                    threading_1_color)
        self.threading = np.zeros((self.controller.num_frames, self.controller.num_motors), dtype=int)

        # resize the tie-up, return everything to zeros
        self.tieup_canvas.delete("all")
        self.tieup_canvas.config(height=(block_size + buffer) * self.controller.num_frames,
                                 width=(block_size + buffer) * self.controller.num_pedals + buffer)
        self.tie_up_text, self.tie_up_rects = populate_matrix(self.tieup_canvas, self.controller.num_frames,
                                                              self.controller.num_pedals, tie_up_0_color,
                                                              tie_up_1_color)
        self.tie_up = np.zeros((self.controller.num_frames, self.controller.num_pedals), dtype=int)

        # rebind buttons with new thing
        self.threading_canvas.bind('<Button-1>',
                                   lambda event, canvas=self.threading_canvas, matrix=self.threading,
                                          text=self.threading_text, rects=self.threading_rects:
                                   self.onMatClick(canvas, matrix, text, event, threading_0_color,
                                                   threading_1_color, rects))
        self.tieup_canvas.bind('<Button-1>',
                               lambda event, canvas=self.tieup_canvas, matrix=self.tie_up,
                                      text=self.tie_up_text, rects=self.tie_up_rects:
                               self.onMatClick(canvas, matrix, text, event, tie_up_0_color, tie_up_1_color, rects))

        # Reposition Pattern & Treadling Canvas
        rel_diff = abs(newHeight - oldHeight) / weave1_height
        new_base_height = 0.22 + self.threading_canvas.winfo_height() / weave1_height
        dynamic_x = (block_size + buffer) * self.controller.num_motors + buffer

        if newHeight > oldHeight:
            self.pattern_canvas.place(relx=0.05, rely=new_base_height + rel_diff)
            self.treadling_canvas.place(x=dynamic_x + 100, rely=new_base_height + rel_diff)
        elif newHeight != oldHeight:
            self.pattern_canvas.place(relx=0.05, rely=new_base_height - rel_diff)
            self.treadling_canvas.place(x=dynamic_x + 100, rely=new_base_height - rel_diff)

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


def toggle_side_nav(self):
    self.side_nav_state = bool(not (self.side_nav_state))

    if self.side_nav_state == True:
        self.notebook.add(self.weave_term, text="Weaving Terminology")
        self.notebook.add(self.weave_draft, text="Weaving Draft Legend")
        self.notebook.add(self.cult_patterns, text="Simple & Cultural Patterns")
        self.notebook.add(self.linear_alg, text="Linear Algebra Review")
        self.side_nav_frame.place(relx=1, rely=0.05, anchor=tk.NE, width=800)
    else:
        for x in range(0, 4, 1):
            self.notebook.hide(x)

        self.side_nav_frame.place(relx=1, rely=0.05, anchor=tk.NE, width=75)