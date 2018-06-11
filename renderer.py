from PIL import Image
import aggdraw
from svgpathtools import Path, CubicBezier, wsvg, parse_path

from ck import CK

# https://github.com/mathandy/svgpathtools

class Renderer:
    def __init__(self, ck):
        self.ck = ck
        self.paths = self.ck.getPaths()
        self.width = 66

    def step(self):
        self.ck.step()
        self.paths = self.ck.getPaths()

    def generateImg(self):
        img = Image.new("RGB", (600, 600), "white")
        canvas = aggdraw.Draw(img)

        outline = aggdraw.Pen("black", self.width)
        # fill = aggdraw.Brush("black")
        fill = None

        self.draw(canvas, outline, fill)
        self.img = img
        return img

    def draw(self, canvas, outline, fill):
        # Draw C/K
        pathsCK = self.paths['ck']
        pathsLL0 = self.paths['ll0']

        # p0
        ckpath = aggdraw.Path()
        ckpath.moveto(pathsCK[0]['p0'][0], pathsCK[0]['p0'][1])
        for path in pathsCK:
            ckpath.curveto(
                path['c0'][0],
                path['c0'][1],
                path['c1'][0],
                path['c1'][1],
                path['p1'][0],
                path['p1'][1]
            )
            canvas.path(ckpath, outline, fill)

        # Draw L/L0
        lpath = aggdraw.Path()
        lpath.moveto(pathsLL0[0]['p0'][0], pathsLL0[0]['p0'][1])
        for path in pathsLL0:
            lpath.curveto(
                path['c0'][0],
                path['c0'][1],
                path['c1'][0],
                path['c1'][1],
                path['p1'][0],
                path['p1'][1]
            )
            canvas.path(lpath, outline, fill)

        canvas.flush()

    def saveImage(self, fn):
        img = self.generateImg()
        img.save(fn, 'PNG')

    def saveSVG(self, fn):
        pathsCK = self.paths['ck']
        pathsLL0 = self.paths['ll0']

        def getSegment(path):
            return CubicBezier(
                complex(path['p0'][0], path['p0'][1]),
                complex(path['c0'][0], path['c0'][1]),
                complex(path['c1'][0], path['c1'][1]),
                complex(path['p1'][0], path['p1'][1])
            )

        # C/K
        ck = Path(
            getSegment(pathsCK[0]),
            getSegment(pathsCK[1]),
            getSegment(pathsCK[2]),
            getSegment(pathsCK[3])
        )

        # L/L0
        ll0 = Path(getSegment(pathsLL0[0]))

        paths = [ck, ll0]
        pathAttributes = {
            "stroke-width": self.width,
            "stroke": "#000",
            "fill": "#fff"
        }

        svg_attributes = {
            "viewBox": "0 0 600 600",
            "x": "0px",
            "y": "0px"
        }

        attributes = [pathAttributes, pathAttributes]
        wsvg(paths, attributes=attributes, svg_attributes=svg_attributes, filename=fn)
