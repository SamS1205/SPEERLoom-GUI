try:
    import tkinter as tk                # python 3
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk     # python 2
    import tkFont as tkfont  # python 2

import serialCom

cal_width = 1550
cal_height = 700
button_height = int(cal_height/3/2)
text_height = int(cal_height/3/4)

class CalFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.geo = str(cal_width) + "x" + str(cal_height)

        label = tk.Label(self, text="SPEERLoom Calibration", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        instr = tk.Label(self, text="When beginning to weave for the first time, the motors need to start all in the "
                                    "down position. Please move them down and the press the \'Set all motors DOWN\' "
                                    "button.", font='Helvetica 12')
        instr.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Home",
                           command=lambda: controller.show_frame("StartPage"))
        button1.pack()
        button2 = tk.Button(self, text="Set all motors DOWN", command=lambda: serialCom.calibrate_all())
        button2.pack()

        self.button_width = int(cal_width / self.controller.num_motors / 2)
        pixel = tk.PhotoImage(width=1, height=1)
        self.image = pixel
        self.up_buttons = []
        self.down_buttons = []
        self.motor_labels = []
        for i in range(self.controller.num_motors):
            self.up_buttons.append(tk.Button(self, text="^", font='Helvetica 15 bold',
                                             command=lambda i=i: serialCom.move_motor(i + 1, serialCom.NOCALIBRATION,
                                                                                      serialCom.UP,
                                                                                      serialCom.CALIBRATE),
                                             image=pixel, compound="c"))
            self.down_buttons.append(
                tk.Button(self, text="v", font='Helvetica 15 bold',
                          command=lambda i=i: serialCom.move_motor(i + 1, serialCom.NOCALIBRATION, serialCom.DOWN,
                                                                   serialCom.CALIBRATE),
                          image=pixel, compound="c"))
            self.motor_labels.append(tk.Label(self, text=str(i+1), font='Helvetica 14 bold',
                                              justify=tk.CENTER, image=pixel, compound="c"))


    def on_resize(self):
        global cal_width, cal_height, button_height
        cal_width = self.controller.winfo_width()
        cal_height = self.controller.winfo_height()
        self.button_width = int(cal_width / self.controller.num_motors / 2)
        button_height = int(cal_height / 3 / 2)
        text_height = int(cal_height/3/4)
        for i in range(len(self.up_buttons)):
            self.down_buttons[i].config(height=button_height, width=self.button_width)
            down_y = cal_height / 4 * 3-button_height/2
            self.down_buttons[i].place(x=cal_width / self.controller.num_motors * i + self.button_width / 2, y=down_y)
            self.motor_labels[i].config(height=text_height, width=self.button_width)
            self.motor_labels[i].place(x=cal_width / self.controller.num_motors * i + self.button_width / 2,
                                       y=down_y - text_height * 3 / 2)
            self.up_buttons[i].config(height=button_height, width=self.button_width)
            self.up_buttons[i].place(x=cal_width / self.controller.num_motors * i + self.button_width / 2,
                                     y=down_y - text_height * 2 - button_height)