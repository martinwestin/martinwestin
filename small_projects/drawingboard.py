
from tkinter import *
from tkinter.colorchooser import askcolor


class Paint:

    DEFAULT_COLOUR = 'black'

    def __init__(self):
        self.root = Tk()

        self.canvas = Canvas(self.root, bg='white', height=800, width=1000)
        self.canvas.pack()

        self.colour_btn = Button(self.canvas, text="Colour", command=lambda: self.choose_colour())
        self.colour_btn.place(relx=0.05, rely=0)

        self.eraser_btn = Button(self.canvas, text="Eraser", command=lambda: self.use_eraser())
        self.eraser_btn.place(relx=0.2, rely=0)

        self.pen_btn = Button(self.root, text="Draw", command=lambda: self.use_pen())
        self.pen_btn.place(relx=0.5, rely=0)

        self.clear_btn = Button(self.canvas, text="Clear", command=lambda: self.clear())
        self.clear_btn.place(relx=0.35, rely=0)

        self.choose_size = Scale(self.canvas, from_=1, to=30, orient=HORIZONTAL)
        self.choose_size.place(relx=0.7, rely=0)

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size.get()
        self.colour = self.DEFAULT_COLOUR
        self.eraser_on = False
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)


    def choose_colour(self):
        self.eraser_on = False
        self.colour = askcolor(color=self.colour)[1]
    
    def clear(self):
        self.eraser_on = False
        self.canvas.delete("all")

    def use_eraser(self):
        self.activate_button(self.eraser_btn, eraser_mode=True)
    
    def use_pen(self):
        self.activate_button(self.pen_btn)

    def activate_button(self, some_button, eraser_mode=False):

        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = self.choose_size.get()
        if self.eraser_on:
            paint_colour = "white"
        else:
            paint_colour = self.colour

        if self.old_x and self.old_y:
            self.canvas.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_colour,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None


Paint()
