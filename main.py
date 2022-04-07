import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import tkinter as tk
from tkinter import ttk
import config
import numpy as np
import time
from logic import App
import threading
matplotlib.style.use('ggplot')

# Todo:
# 1. Create class for Gui
# 2. Create class for logic


class GUI(App):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.build()
    def build(self):
        plt.ion()

        self.root = tk.Tk()
        self.root.geometry(f'{self.width}x{self.height}')
        self.root.resizable=(False, False)
        # self.root['bg'] = (255,255,255)

        # frame_left_st = ttk.Style()
        # frame_left_st.configure('LeftFrame.TFrame', background='green')
        # frame_right_st = ttk.Style()
        # frame_right_st.configure('RightFrame.TFrame', background='red')

        fr_left_width = self.width/3
        frame_left = ttk.Frame(self.root, style='LeftFrame.TFrame', width=fr_left_width, height=self.height)
        frame_left.pack_propagate(0)
        frame_left.pack(side='left')

        fr_right_size = self.width - fr_left_width
        frame_right = ttk.Frame(self.root, style='RightFrame.TFrame', width=fr_right_size, height=self.height)
        frame_right.pack_propagate(0)
        frame_right.pack()

        scalers_div__width = fr_left_width - fr_left_width / 4
        scalers_div__height = self.height  / 3
        scalers_div = ttk.Frame(frame_left, style='RightFrame.TFrame', width=scalers_div__width, height=scalers_div__height)
        scalers_div.pack_propagate(0)
        scalers_div.place(anchor='center', x=fr_left_width/2, y=self.height/4)

        scaler_lbl = ttk.Label(scalers_div, text ='Number of Tosses: 25')
        scaler_lbl.pack_propagate(0)
        scaler_lbl.pack()

        self.tosses_value = tk.DoubleVar()
        self.tosses_value.set(25)
        scaler1 = ttk.Scale(scalers_div, from_=0, to=200, length=200, value=self.tosses_value.get(), cursor='left_ptr',
                             command= lambda val: self.__update_scaler(val, scaler_lbl, 1), variable=self.tosses_value)

        scaler1.pack_propagate(0)
        scaler1.pack()

        self.scaler_value = tk.DoubleVar()
        self.scaler_value.set(0.5)
        scaler_lbl2 = ttk.Label(scalers_div, text =f'Probability oh Heads: {self.scaler_value.get()}')
        scaler_lbl2.pack_propagate(0)
        scaler_lbl2.pack()

        scaler2 = ttk.Scale(scalers_div, from_=0.1, to=1.0, length=200, value=0.5 ,cursor='left_ptr',
                            variable=self.scaler_value, command=lambda val: self.__update_scaler(val, scaler_lbl2,2))
        scaler2.pack_propagate(0)
        scaler2.pack()



        btns_div__width = fr_left_width - fr_left_width / 4
        btns_div__height = self.height  / 2.5
        btns_div = ttk.Frame(frame_left, style='RightFrame.TFrame', width=btns_div__width, height=btns_div__height)
        btns_div.pack_propagate(0)
        btns_div.place(anchor='center', x=fr_left_width/2, y=self.height/2 + self.height/6)


        draw_btn_y = btns_div__height/3
        draw_btn = ttk.Button(btns_div, text='Toss', command=self.__update_plot)
        draw_btn.pack_propagate(0)
        draw_btn.place(anchor='center', x=btns_div__width/2, y=draw_btn_y, width=fr_left_width/2, height=self.height*0.1)

        clear_btn = ttk.Button(btns_div, text='Reset', command=self.__reset)
        clear_btn.pack_propagate(0)
        clear_btn.place(anchor='center', x=btns_div__width/2, y=draw_btn_y*2, width=fr_left_width/2, height=self.height*0.1)

        self.fig = Figure(figsize=(6,6))
        self.ax = self.fig.add_subplot(111)
        self.ax.set_ylim([0,1])

        # self.ax.plot(self.counts['H'], self.counts['T'], scaley=False, color='blue')
        artist, = self.ax.plot(self.counts['H'], self.counts['T'], animated=True,scaley=False, color='blue') # Line2D artist
        # self.ax.draw_artist(artist)


        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_right)
        self.canvas.get_tk_widget().pack()


        self.x_counter=0
        self.x_vals=[]
        self.y_vals=[]
        threading.Thread(target=self.helper).start()

    def __reset(self):
        self.counts = {'H':1, 'T':1}
        self.ax.clear()
        self.x_vals=[]
        self.y_vals=[]
        self.x_counter=0

    def helper(self):
        while True:
            self.canvas.draw()

    def __update_plot(self):
        for i in range(int(self.tosses_value.get())):
            self.generate_prediction(self.scaler_value.get())
            proportion = self.counts['H']/(self.counts['H']+self.counts['T'])
            self.x_counter+=1
            self.x_vals.append(self.x_counter)
            self.y_vals.append(proportion)
            # self.ax.set_xdata(i)
            # self.ax.set_ydata(proportion)
            artist, = self.ax.plot(self.x_vals, self.y_vals, scaley=False, animated=True, color='blue')
            # plt.show(block=False)
            # plt.pause(0.1)
            # self.ax.plot(self.x_vals, self.y_vals, scaley=False, color='blue')
            self.ax.draw_artist(artist)

            # self.ax.draw_artist(artist)


        self.x_vals=[self.x_vals[-1]]
        self.y_vals=[self.y_vals[-1]]

    def __update_scaler(self, value, lbl, scale_number):
        if scale_number==1:
            value_list = [1,2,5,10,15,25,50,100,200] # compare values of scaler2 and adjust
            value = float(value)
            upper_bound = None
            for i in range(len(value_list)):
                if value_list[i]>=value:
                    upper_bound = i
                    break
            if upper_bound==0:
                self.tosses_value.set(value_list[0])
            else:
                avg = (value_list[upper_bound]+value_list[upper_bound-1])/2
                if value>=avg:
                    self.tosses_value.set(value_list[upper_bound])
                else:
                    self.tosses_value.set(value_list[upper_bound-1])

            lbl['text']=f'Number of Tosses: {int(self.tosses_value.get())}'
        else:
            self.scaler_value.set(value)
            lbl['text']='Probability oh Heads: %.2f' % self.scaler_value.get()





if __name__=='__main__':
    window = GUI(config.width, config.height)
    tk.mainloop()
