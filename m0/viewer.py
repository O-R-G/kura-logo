import tkinter as tk
from PIL import ImageTk
import time

from renderer import Renderer

class Viewer:
    def __init__(self, renderer, fps):
        self.root = tk.Tk()
        self.root.title('Kura/Cura')
        self.renderer = renderer
        self.fps = 1000/fps

        tmp = ImageTk.PhotoImage(self.renderer.generateImg())
        w = tmp.width()
        h = tmp.height()

        x = 0
        y = 0

        self.root.geometry("%dx%d+%d+%d" % (w, h, x, y))

        self.panel1 = tk.Label(self.root, image=tmp)
        self.panel1.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

        self.root.after(int(self.fps * 1000), self.render)
        self.root.mainloop()


    def render(self):
        self.renderer.step()
        tmp = ImageTk.PhotoImage(self.renderer.generateImg())
        self.panel1.configure(image=tmp)
        self.panel1.image = tmp
        self.root.after(self.fps, self.render)
