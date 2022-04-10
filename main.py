import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import tkinter.font as font
import config
from App import App
import os

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

try:
    from tkinter import ttk
except ImportError:
    import ttk

matplotlib.style.use('ggplot')

class GUI(App):
    FONT_NAME = 'LilyUPC'
    def __init__(self, width, height, interv_ms=10):
        super().__init__(width, height)
        self.frame_counter = -1 # initial value
        self.frames = 200
        self.interv_ms = interv_ms
        self.x_counter = 0 # to increase x-axis
        self.__x_vals = []
        self.__y_vals = []
        self.build()

    def get_xs(self):
        return self.__x_vals

    def get_ys(self):
        return self.__y_vals

    def build(self):

        root = tk.Tk()
        root.title('Law of Large Numbers Simulation')
        root.geometry(f'{self.width}x{self.height}')
        root.resizable(False, False)

        # Font configurations
        btn_label__font = font.Font(root=root, font=(GUI.FONT_NAME,10))
        check_btn__font = font.Font(family=GUI.FONT_NAME, size=10, slant='italic')
        check_button__style = ttk.Style()
        check_button__style.configure('main.TCheckbutton',font=check_btn__font)
        click_button__style = ttk.Style()
        click_button__style.configure('main.TButton', font=btn_label__font)

        # Frames
        fr_left_width = self.width/3
        frame_left = ttk.Frame(root, width=fr_left_width, height=self.height)
        frame_left.pack_propagate(0)
        frame_left.pack(side='left')

        fr_right_size = self.width - fr_left_width
        frame_right = ttk.Frame(root,  width=fr_right_size, height=self.height)
        frame_right.pack_propagate(0)
        frame_right.pack()


        # Divs
        scalers_div__width = fr_left_width - fr_left_width / 4
        scalers_div__height = self.height  / 3
        scalers_div = ttk.Frame(frame_left,
                                width=scalers_div__width,
                                height=scalers_div__height)
        scalers_div.pack_propagate(0)
        scalers_div.place(anchor='center',
                          x=fr_left_width/2,
                          y=self.height/4)

        mutual_pady = scalers_div__height/16
        tosses_div = ttk.Frame(scalers_div,
                               width=scalers_div__width,
                               height=scalers_div__height/2)
        tosses_div.pack_propagate(0)
        tosses_div.pack()

        # Tosses label
        tosses_lbl = ttk.Label(tosses_div,
                               font=btn_label__font,
                               text ='Number of Tosses: 25')
        tosses_lbl.pack_propagate(0)
        tosses_lbl.pack()

        # Tosses scaler
        self.tosses_value = tk.DoubleVar()
        self.tosses_value.set(25)
        tosses_scaler = ttk.Scale(tosses_div,
                                  from_=0,
                                  to=200,
                                  length=200,
                                  value=self.tosses_value.get(),
                                  command= lambda val: self.__update_scaler(val, tosses_lbl, 1), variable=self.tosses_value)

        tosses_scaler.pack_propagate(0)
        tosses_scaler.pack(pady=mutual_pady)

        probability_div = ttk.Frame(scalers_div,
                                    width=scalers_div__width,
                                    height=scalers_div__height/2)
        probability_div.pack_propagate(0)
        probability_div.pack()

        # Probability label
        self.probability_value = tk.DoubleVar()
        self.probability_value.set(0.5)
        probability_lbl = ttk.Label(probability_div,
                                    font=btn_label__font,
                                    text =f'Probability of Heads: {self.probability_value.get()}')
        probability_lbl.pack_propagate(0)
        probability_lbl.pack()

        # Probability scaler
        probability_scaler = ttk.Scale(probability_div,
                                       from_=0.1,
                                       to=1.0,
                                       length=200,
                                       value=0.5,
                                       variable=self.probability_value,
                                       command=lambda val: self.__update_scaler(val, probability_lbl,2))
        probability_scaler.pack_propagate(0)
        probability_scaler.pack(pady=mutual_pady)

        # Checkbox for average line
        self.help_line_is_shown = tk.BooleanVar()
        self.help_line_is_shown.set(False)
        show_avg_line = ttk.Checkbutton(probability_div,
                                        text='Show line',
                                        style='main.TCheckbutton',
                                        variable=self.help_line_is_shown,
                                        command=self.show_line)
        show_avg_line.pack_propagate(0)
        show_avg_line.pack(side='bottom')

        # Div for buttons
        btns_div__width = fr_left_width - fr_left_width / 4
        btns_div__height = self.height  / 2.5
        btns_div = ttk.Frame(frame_left,
                             width=btns_div__width,
                             height=btns_div__height)
        btns_div.pack_propagate(0)
        btns_div.place(anchor='center',
                       x=fr_left_width/2,
                       y=self.height/2 + self.height/6)

        self.fig = Figure(figsize=(6,6))
        self.ax = self.fig.add_subplot(111)
        self.ax.set_ylim([0,1])
        self.ax.plot(self.counts['H'],
                     self.counts['T'],
                     scaley=False,
                     color='blue')
        self.ax.set_xlabel('Tosses')
        self.ax.set_ylabel('Overall Percentage of Heads')
        self.canvas = FigureCanvasTkAgg(self.fig,
                                        master=frame_right)
        self.canvas.get_tk_widget().pack()
        self.MyAnimation = FuncAnimation(self.fig,
                                         self.__animate,
                                         init_func=self.__initilize_animation,
                                         interval = self.interv_ms,
                                         frames=self.frames)
        # Toss Button
        draw_btn_y = btns_div__height/3
        draw_btn = ttk.Button(btns_div,
                              style='main.TButton',
                              text='Toss',
                              command=self.MyAnimation.resume)
        draw_btn.pack_propagate(0)
        draw_btn.place(anchor='center',
                       x=btns_div__width/2,
                       y=draw_btn_y - draw_btn_y * 0.5,
                       width=fr_left_width/2,
                       height=self.height*0.1)
        # Reset Button
        clear_btn = ttk.Button(btns_div,
                               style='main.TButton',
                               text='Reset',
                               command=self.__reset)
        clear_btn.pack_propagate(0)
        clear_btn.place(anchor='center',
                        x=btns_div__width/2,
                        y=draw_btn_y*2- draw_btn_y * 0.65,
                        width=fr_left_width/2,
                        height=self.height*0.1)
        # Save Button
        save_btn = ttk.Button(btns_div,
                              style='main.TButton',
                              text='Save',
                              command=self.__save)
        save_btn.pack_propagate(0)
        save_btn.place(anchor='center',
                       x=btns_div__width/2,
                       y=draw_btn_y*3 - draw_btn_y * 0.8,
                       width=fr_left_width/2,
                       height=self.height*0.1)


    def show_line(self):
        """
        function to toggle red line
        """
        if self.help_line_is_shown.get():
            self.artist_line, =self.ax.plot([0, self.x_counter+1], [0.5, 0.5], c='r')
        else:
            self.artist_line.remove()
        self.canvas.draw()
    def __reset(self):
        """
        function to reset and redraw later
        """
        self.MyAnimation.pause()
        self.help_line_is_shown.set(False)
        self.counts = {'H':1, 'T':1}
        self.frame_counter=0
        self.__x_vals=[]
        self.__y_vals=[]
        self.x_counter=0
        self.ax.clear()
        self.ax.set_ylim([0,1])
        self.canvas.draw()
    @staticmethod
    def generate_file_number():
        """
        function to exclude possibility of file replacing previous self when saving
        :return: filen number
        """
        try:
            pwd = os.path.join(os.getcwd(), 'BigNum__plots')
            filenames = os.walk(pwd)
            number = int(list(filenames)[0][-1][-1].split('.')[0][-1]) # grab the number from the file
        except (ValueError,IndexError, AttributeError):
            number = 0
        return number + 1
    def __save(self):
        """
        save file
        """
        file_end_number = GUI.generate_file_number()
        if os.path.exists(os.path.join(os.getcwd(),'BigNum__plots')):
            self.fig.savefig(f'BigNum__plots/bigNumPlot_{file_end_number}.jpg')
        else:
            os.mkdir('BigNum__plots')
            self.fig.savefig(f'BigNum__plots/bigNumPlot_{file_end_number}.jpg')

    def __initilize_animation(self):
        """
        to initialize FuncAnimation
        """
        self.MyAnimation.pause()

    def __animate(self,i=None):
        try:
            if self.frame_counter!=-1:
                self.generate_prediction(self.probability_value.get())
                proportion = self.counts['H']/(self.counts['H']+self.counts['T'])
                self.x_counter+=1

                if self.help_line_is_shown.get():
                    self.artist_line.set_data([0, self.x_counter], [0.5, 0.5])
                self.__x_vals.append(self.x_counter)
                self.__y_vals.append(proportion)
                self.ax.plot(self.__x_vals,
                             self.__y_vals,
                             scaley=False,
                             color='blue')

                self.fig.canvas.draw_idle()
                self.fig.canvas.flush_events()

                self.__x_vals=[self.__x_vals[-1]]
                self.__y_vals=[self.__y_vals[-1]]
                self.frame_counter+=1

                if self.frame_counter==self.tosses_value.get():
                    self.frame_counter=0
                    self.MyAnimation.pause()
                return
            self.frame_counter=0
            self.MyAnimation.pause()
        except IndexError:
            return
    def __update_scaler(self, value, lbl, scaler_number):
        """
        function to add steps to scalers and update labels
        :param value: current scaler value
        :param lbl: label to that scaler
        :param scaler_number:
                1 - Toss Number Scaler
                2 - Probability Scaler
        """
        if scaler_number==1:
            value_list = [1,2,5,10,15,25,50,100,200] # compare values of probability_scaler and adjust
            value, upper_bound = self.__set_scaler(value, value_list)
            if upper_bound==0:
                self.tosses_value.set(value_list[0])
            else:
                avg = (value_list[upper_bound]+value_list[upper_bound-1])/2
                if value>=avg:
                    self.tosses_value.set(value_list[upper_bound])
                else:
                    self.tosses_value.set(value_list[upper_bound-1])
            lbl['text']=f'Number of Tosses: {int(self.tosses_value.get())}'

        elif scaler_number==2:
            self.probability_value.set(value)
            lbl['text']='Probability of Heads: %.2f' % self.probability_value.get()


    def __set_scaler(self, value,value_list):
        """
        Get next value in list compared to scaler value
        :param value: scaler value
        :param value_list: list for ticks
        :return: casted to float scaler value, next value to scaler's value in list
        """
        value = float(value)
        upper_bound = None
        for i in range(len(value_list)):
            if value_list[i]>=value:
                upper_bound = i
                break
        return value, upper_bound

if __name__=='__main__':
    window = GUI(config.WIDTH, config.HEIGHT)
    tk.mainloop()
