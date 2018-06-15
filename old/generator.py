#  DEPRACATED

from __future__ import division, print_function
from svgpathtools import Path, CubicBezier, wsvg, parse_path

# https://github.com/mathandy/svgpathtools
# http://spencermortensen.com/articles/bezier-circle/
# https://math.stackexchange.com/questions/1294938/explicit-bezier-curves-lerping-between-curves-same-as-lerping-control-points

# c = parse_path('M516.4,424.9C473.2,499.6,392.4,549.8,300,549.8C162,549.8,50.2,438,50.2,300S162,50.2,300,50.2c92.4,0,173.2,50.2,216.4,124.9')
# k = parse_path('M300.5,549.8L175.6,424.9L50.7,300l124.9-124.9L300.5,50.2')

class Generator:
    c = [
        {'start': 566.4+424.9j, 'c1': 523.2+499.6j, 'c2': 442.4+549.8j, 'end': 350+549.8j},
        {'start': 350+549.8j, 'c1': 212+549.8j, 'c2': 100.2+438j, 'end': 100.2+300j},
        {'start': 100.2+300j, 'c1': 100.2+162j, 'c2': 212+50.2j, 'end': 350+50.2j},
        {'start': 350+50.2j, 'c1': 442.4+50.2j, 'c2': 523.2+100.4j, 'end': 566.4+175.1j}
    ]
    k = [
        {'start': 350.5+549.8j, 'c1': 288.05+487.35j, 'c2': 288.05+487.35j, 'end': 225.6+424.9j},
        {'start': 225.6+424.9j, 'c1': 163.15+362.45j, 'c2': 163.15+362.5j, 'end': 100.7+300j},
        {'start': 100.7+300j, 'c1': 163.15+237.55j, 'c2': 163.15+237.55j, 'end': 225.6+175.1j},
        {'start': 225.6+175.1j, 'c1': 288.05+112.65j, 'c2': 288.05+112.65j, 'end': 350.5+50.2j}
    ]

    l = {'start': 35.7+50.2j, 'c1':35.7+300j, 'c2':35.7+300j, 'end': 35.7+549.8j}
    l0 = {'start': 35.7+300j, 'c1':35.7+300j, 'c2':35.7+300j, 'end': 35.7+300j}

    paths = []
    width = 0

    def lerp(self, p1, p2, t):
        return (1-t)*p1 + t*p2

    def getSegment(self, c, k, idx, t):
        return CubicBezier(
            self.lerp(c[idx]['start'], k[idx]['start'], t),
            self.lerp(c[idx]['c1'], k[idx]['c1'], t),
            self.lerp(c[idx]['c2'], k[idx]['c2'], t),
            self.lerp(c[idx]['end'], k[idx]['end'], t))

    def generate(self, u, v, w):
        seg1 = self.getSegment(self.c, self.k, 0, u)
        seg2 = self.getSegment(self.c, self.k, 1, u)
        seg3 = self.getSegment(self.c, self.k, 2, u)
        seg4 = self.getSegment(self.c, self.k, 3, u)

        ck = Path(seg1,seg2,seg3,seg4)

        ll0 = Path(CubicBezier(
                self.lerp(self.l['start'], self.l0['start'], v),
                self.lerp(self.l['c1'],self.l0['c1'], v),
                self.lerp(self.l['c2'],self.l0['c2'], v),
                self.lerp(self.l['end'],self.l0['end'], v)
            ))

        self.paths = [ck, ll0]
        self.width = w

    def save(self, filename):
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
        wsvg(self.paths, attributes=attributes, svg_attributes=svg_attributes, filename=filename)
