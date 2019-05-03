import tkinter as tk
from PIL import ImageTk
import time

from renderer import Renderer

class Viewer:
    def __init__(self, renderer, fps, output = None):
        self.root = tk.Tk()
        self.root.title('Kura/Cura')
        self.renderer = renderer
        self.fps = int(1000/fps)

        self.frame = 0
        self.output = output

        tmp = ImageTk.PhotoImage(self.renderer.generateImg())
        self.checkOutput()

        w = tmp.width()
        h = tmp.height()

        x = 0
        y = 0

        self.root.geometry("%dx%d+%d+%d" % (w, h, x, y))

        self.panel1 = tk.Label(self.root, image=tmp)
        self.panel1.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

        self.root.after(self.fps, self.render)
        self.root.mainloop()


    def render(self):
        self.frame = self.frame + 1
        result = self.renderer.step()

        tmp = ImageTk.PhotoImage(self.renderer.generateImg())
        self.checkOutput()

        self.panel1.configure(image=tmp)
        self.panel1.image = tmp
        if result == True:
            self.root.after(self.fps, self.render)

    def checkOutput(self):
        if self.output == "svg":
            self.renderer.saveSVG('out/' + str(self.frame) + '.svg')
        elif self.output == "png":
            self.renderer.saveImage('out/' + str(self.frame) + '.png')
        else:
            return
