from __future__ import division, print_function
from svgpathtools import Path, CubicBezier, wsvg, parse_path
import random

# https://github.com/mathandy/svgpathtools
# http://spencermortensen.com/articles/bezier-circle/
# https://math.stackexchange.com/questions/1294938/explicit-bezier-curves-lerping-between-curves-same-as-lerping-control-points

c = parse_path('M516.4,424.9C473.2,499.6,392.4,549.8,300,549.8C162,549.8,50.2,438,50.2,300S162,50.2,300,50.2c92.4,0,173.2,50.2,216.4,124.9')
k = parse_path('M300.5,549.8L175.6,424.9L50.7,300l124.9-124.9L300.5,50.2')

c = [
    {'start': 516.4+424.9j, 'c1': 473.2+499.6j, 'c2': 392.4+549.8j, 'end': 300+549.8j},
    {'start': 300+549.8j, 'c1': 162+549.8j, 'c2': 50.2+438j, 'end': 50.2+300j},
    {'start': 50.2+300j, 'c1': 50.2+162j, 'c2': 162+50.2j, 'end': 300+50.2j},
    {'start': 300+50.2j, 'c1': 392.4+50.2j, 'c2': 473.2+100.4j, 'end': 516.4+175.1j}
]
k = [
    {'start': 300.5+549.8j, 'c1': 238.05+487.35j, 'c2': 238.05+487.35j, 'end': 175.6+424.9j},
    {'start': 175.6+424.9j, 'c1': 113.15+362.45j, 'c2': 113.15+362.5j, 'end': 50.7+300j},
    {'start': 50.7+300j, 'c1': 113.15+237.55j, 'c2': 113.15+237.55j, 'end': 175.6+175.1j},
    {'start': 175.6+175.1j, 'c1': 238.05+112.65j, 'c2': 238.05+112.65j, 'end': 300.5+50.2j}
]

l = {'start': -15.7+50.2j, 'c1':-15.7+300j, 'c2':-15.7+300j, 'end': -15.7+549.8j}
l0 = {'start': -15.7+300j, 'c1':-15.7+300j, 'c2':-15.7+300j, 'end': -15.7+300j}

def lerp(p1, p2, t):
    return (1-t)*p1 + t*p2

def getSegment(c, k, idx, t):
    return CubicBezier(
        lerp(c[idx]['start'], k[idx]['start'], t),
        lerp(c[idx]['c1'],k[idx]['c1'], t),
        lerp(c[idx]['c2'],k[idx]['c2'], t),
        lerp(c[idx]['end'],k[idx]['end'], t))

def generate(u, v, x, y, idx):
    seg1 = getSegment(c, k, 0, 1-u)
    seg2 = getSegment(c, k, 1, 1-u)
    seg3 = getSegment(c, k, 2, 1-u)
    seg4 = getSegment(c, k, 3, 1-u)

    ck = Path(seg1,seg2,seg3,seg4)

    ll0 = Path(CubicBezier(
            lerp(l['start'], l0['start'], v),
            lerp(l['c1'],l0['c1'], v),
            lerp(l['c2'],l0['c2'], v),
            lerp(l['end'],l0['end'], v)
        ))

    pathAttributes = {
        "stroke-width": x,
        "stroke": "#000",
        "fill": "#fff"
    }

    pathAttributesl = {
        "stroke-width": y,
        "stroke": "#000",
        "fill": "#fff"
    }

    svg_attributes = {
        "viewBox": "0 0 600 600",
        "x": "0px",
        "y": "0px"
    }

    paths = [ck, ll0]
    attributes = [pathAttributes, pathAttributesl]
    wsvg(paths, attributes=attributes, svg_attributes=svg_attributes, filename='run/output' + str(idx+50) + '.svg')

def bind(value, lower, upper):
    if value < lower:
        return lower
    if value > upper:
        return upper
    return value

# run
steps = 50
stepsize = 0.02
u = random.uniform(0, 1)
v = random.uniform(0, 1)
x = random.uniform(1, 100)
y = random.uniform(1, 100)
for t in range(0, steps+1):
    generate(u, v, x, y, t)


    if random.uniform(0, 1) > 0.5:
        u = u + stepsize
    else:
        u = u - stepsize

    if random.uniform(0, 1) > 0.5:
        v = v + stepsize
    else:
        v = v - stepsize

    if random.uniform(0, 1) > 0.5:
        x = x + 5
    else:
        x = x - 5

    if random.uniform(0, 1) > 0.5:
        y = y + 5
    else:
        y = y - 5

    u = bind(u, 0, 1)
    v = bind(v, 0, 1)
    x = bind(x, 1, 100)
    y = bind(y, 1, 100)
