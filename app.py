try:
    import tkinter as tk                # python 3
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk     # python 2
    import tkFont as tkfont  # python 2

from constants import *
from startFrame import StartPage
from weaveFrame1 import WeaveFrame1
from calFrame import CalFrame
from weaveFrame2 import WeaveFrame2
from fileframe import FileFrame
from resetFrame import ResetFrame
from mathMode_WelcomePage import MathMode_WelcomePage
from mathMode_Page1 import MathMode_Page1
from mathMode_Page2 import MathMode_Page2

class App(tk.Tk):

    def __init__(self, gui_args, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.bind("<Configure>", self.resize)
        self.num_motors = gui_args[0]
        self.pat_len2 = gui_args[2]
        self.num_frames = gui_args[3]
        self.num_pedals = gui_args[4]

        # the container is where we'll stack a bunch of frames on top of each other,
        # then the one we want visible will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.page_names = []
        for F in (StartPage, CalFrame, MathMode_WelcomePage, MathMode_Page1, MathMode_Page2, WeaveFrame1, WeaveFrame2, FileFrame, ResetFrame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            self.page_names.append(page_name)

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def get_page(self, page_class):
       return self.frames[page_class]

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        self.geometry(frame.geo)

        if page_name == "MathMode_WelcomePage":
            frame.controller.maxsize(mathMode_width,mathMode_height)
            frame.controller.resizable(0,0)
        elif page_name == "MathMode_Page1" or page_name == "MathMode_Page2":
            frame.controller.maxsize(mathMode_width,mathMode_height_2)
            frame.controller.resizable(0,0)
        elif page_name == "StartPage": 
            frame.controller.minsize(start_width,start_height)
            frame.controller.maxsize(start_width,start_height)
            frame.controller.resizable(0,0)
        elif page_name == "ResetFrame": 
            frame.controller.maxsize(reset_width,reset_height)
            frame.controller.resizable(0,0)
        elif page_name == "CalFrame":
            frame.controller.minsize(cal_min_width,cal_min_height)
            frame.controller.maxsize(cal_width,cal_height)
            frame.controller.resizable(1,1)
        elif page_name == 'WeaveFrame1':
            frame.controller.minsize(weave1_width,weave1_height)
            frame.controller.maxsize(1920,1080) 
            frame.controller.resizable(1,1)         
        else:
            frame.controller.maxsize(1920,1080)
            frame.controller.resizable(1,1)

    def resize(self, event):
        for page_name in self.page_names:
            resize_method = getattr(self.frames[page_name], "on_resize", None)
            if callable(resize_method):
                self.frames[page_name].on_resize()