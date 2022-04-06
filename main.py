import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import config

# Todo:
# 1. Create class for Gui
# 2. Create class for logic



class Window:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.build()
    def build(self):
        self.root = tk.Tk()
        self.root.geometry(f'{self.width}x{self.height}')
        self.root.resizable=(False, False)
        # self.root['bg'] = (255,255,255)

        frame_left_st = ttk.Style()
        frame_left_st.configure('LeftFrame.TFrame', background='green')
        frame_right_st = ttk.Style()
        frame_right_st.configure('RightFrame.TFrame', background='red')

        fr_left_width = self.width/3
        frame_left = ttk.Frame(self.root, style='LeftFrame.TFrame', width=fr_left_width, height=self.height)
        frame_left.pack_propagate(0)
        frame_left.pack(side='left')

        fr_right_size =self.width - fr_left_width
        frame_right = ttk.Frame(self.root, style='RightFrame.TFrame', width=fr_right_size, height=self.height)
        frame_right.pack_propagate(0)
        frame_right.pack()

        scalers_div__width = fr_left_width - fr_left_width / 4
        scalers_div__height = self.height  / 3
        scalers_div = ttk.Frame(frame_left, style='RightFrame.TFrame', width=scalers_div__width, height=scalers_div__height)
        scalers_div.pack_propagate(0)
        scalers_div.place(anchor='center', x=fr_left_width/2, y=self.height/4)


        scaler_lbl = ttk.Label(scalers_div, text ='Probability oh Heads:')
        scaler_lbl.pack_propagate(0)
        scaler_lbl.pack()

        scaler1 = ttk.Scale(scalers_div, from_=0.1, to=1.0, length=200, value=0.5, cursor='left_ptr')
        scaler1.pack_propagate(0)
        scaler1.pack()

        scaler_lbl2 = ttk.Label(scalers_div, text ='Number of Tosses:')
        scaler_lbl2.pack_propagate(0)
        scaler_lbl2.pack()

        scaler2 = ttk.Scale(scalers_div, from_=0.1, to=1.0, length=200, value=0.5, cursor='left_ptr')
        scaler2.pack_propagate(0)
        scaler2.pack()



        btns_div__width = fr_left_width - fr_left_width / 4
        btns_div__height = self.height  / 2.5
        btns_div = ttk.Frame(frame_left, style='RightFrame.TFrame', width=btns_div__width, height=btns_div__height)
        btns_div.pack_propagate(0)
        btns_div.place(anchor='center', x=fr_left_width/2, y=self.height/2 + self.height/6)

        button = ttk.Button(btns_div, text='Toss')
        button.pack_propagate(0)
        button.place(anchor='center', x=btns_div__width/2, y=btns_div__height/3, width=fr_left_width/2, height=self.height*0.1)

    @staticmethod
    def update_scaler():
        value_list = [2,5,10,25,50,75,100,150,200] # compare values of scaler2 and adjust
window = Window(config.width, config.height)
tk.mainloop()
