from PIL import Image
import aggdraw
import svgwrite
from ck import CK

# https://svgwrite.readthedocs.io/en/master/
# http://effbot.org/zone/pythondoc-aggdraw.htm

class Renderer:
    def __init__(self, ck):
        self.ck = ck
        self.paths = self.ck.getPaths()
        self.width = 66

    def step(self):
        result = self.ck.step()
        self.paths = self.ck.getPaths()
        return result

    def generateImg(self):
        img = Image.new("RGB", (600, 600), "white")
        canvas = aggdraw.Draw(img)

        outline = aggdraw.Pen('rgb(0, 0, 0)', self.width)
        #outline = aggdraw.Pen("black", self.width)
        # fill = aggdraw.Brush("black")
        fill = None

        self.draw(canvas, outline, fill)
        self.img = img
        return img

    def draw(self, canvas, outline, fill):
        pathdraw = aggdraw.Path()
        ck = []
        ck.extend(self.paths['q1'])
        ck.extend(self.paths['q4'])

        ll0 = []
        ll0.extend(self.paths['q2'])
        ll0.extend(self.paths['q3'])

        for idx, path in enumerate(ck):
            if idx == 0:
                pathdraw.moveto(path['p0'][0], path['p0'][1])
            pathdraw.curveto(
                path['c0'][0],
                path['c0'][1],
                path['c1'][0],
                path['c1'][1],
                path['p1'][0],
                path['p1'][1]
            )
            canvas.path(pathdraw, outline, fill)

        for idx, path in enumerate(ll0):
            if idx == 0:
                pathdraw.moveto(path['p0'][0], path['p0'][1])
            pathdraw.curveto(
                path['c0'][0],
                path['c0'][1],
                path['c1'][0],
                path['c1'][1],
                path['p1'][0],
                path['p1'][1]
            )
            canvas.path(pathdraw, outline, fill)

        canvas.flush()

    def saveImage(self, fn):
        img = self.generateImg()
        img.save(fn, 'PNG')

    def saveSVG(self, fn):
        dwg = svgwrite.Drawing(fn, size = (600, 600), viewBox = ("0 0 600 600"))

        ck = []
        ck.extend(self.paths['q1'])
        ck.extend(self.paths['q4'])

        ll0 = []
        ll0.extend(self.paths['q2'])
        ll0.extend(self.paths['q3'])

        str_list = []
        for idx, path in enumerate(ck):
            if idx == 0:
                str_list.append("M {}, {}".format(path['p0'][0], path['p0'][1]))
            str_list.append("C {}, {}, {}, {}, {}, {}".format(
                path['c0'][0],
                path['c0'][1],
                path['c1'][0],
                path['c1'][1],
                path['p1'][0],
                path['p1'][1]
            ))
        s = ''.join(str_list)
        dwg.add(dwg.path(s).stroke(color="rgb(0%,0%,0%)",width=self.width).fill("none"))

        str_list = []
        for idx, path in enumerate(ll0):
            if idx == 0:
                str_list.append("M {}, {}".format(path['p0'][0], path['p0'][1]))
            str_list.append("C {}, {}, {}, {}, {}, {}".format(
                path['c0'][0],
                path['c0'][1],
                path['c1'][0],
                path['c1'][1],
                path['p1'][0],
                path['p1'][1]
            ))
        s = ''.join(str_list)
        dwg.add(dwg.path(s).stroke(color="rgb(0%,0%,0%)",width=self.width).fill("none"))

        dwg.save()
