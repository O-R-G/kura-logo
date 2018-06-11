import random

# http://spencermortensen.com/articles/bezier-circle/
# https://math.stackexchange.com/questions/1294938/explicit-bezier-curves-lerping-between-curves-same-as-lerping-control-points

class CK:
    c = [
        [(566.4, 424.9), (523.2,499.6), (442.4,549.8), (350,549.8)],
        [(350, 549.8), (212,549.8), (100.2,438), (100.2,300)],
        [(100.2, 300), (100.2,162), (212,50.2), (350,50.2)],
        [(350,50.2), (442.4,50.2), (523.2,100.4), (566.4,175.1)]
    ]
    k = [
        [(350.5,549.8), (288.05,487.35), (288.05,487.35), (225.6,424.9)],
        [(225.6,424.9), (163.15,362.45), (163.15,362.5), (100.7,300)],
        [(100.7,300), (163.15,237.55), (163.15,237.55), (225.6,175.1)],
        [(225.6,175.1), (288.05,112.65), (288.05,112.65), (350.5,50.2)]
    ]
    l = [
        [(35.7,50.2), (35.7,300), (35.7,300), (35.7,549.8)]
    ]
    l0 = [
        [(35.7,300), (35.7,300), (35.7,300), (35.7,300)]
    ]

    stepsize = 0.02

    def __init__(self):
        self.u = random.uniform(0, 1)
        self.v = random.uniform(0, 1)

    def lerp(self, p1, p2, t):
        return ((1-t)*p1[0] + t*p2[0], (1-t)*p1[1] + t*p2[1])

    def bind(self, value, lower, upper):
        if value < lower:
            return lower
        if value > upper:
            return upper
        return value

    def getBezierPointsPartial(self, cval, kval, t):
        p0 = self.lerp(cval[0], kval[0], t)
        c0 = self.lerp(cval[1], kval[1], t)
        c1 = self.lerp(cval[2], kval[2], t)
        p1 = self.lerp(cval[3], kval[3], t)

        return {'p0': p0, 'c0': c0, 'c1': c1, 'p1': p1}

    def getPaths(self):
        ck = []
        for idx in range(len(self.c)):
            ck.append(self.getBezierPointsPartial(self.c[idx], self.k[idx], self.u))

        ll0 = []
        for idx in range(len(self.l)):
            ll0.append(self.getBezierPointsPartial(self.l[idx], self.l0[idx], self.v))

        return {'ck': ck, 'll0': ll0}

    def step(self):
        if random.uniform(0, 1) > 0.5:
            self.u = self.u + self.stepsize
        else:
            self.u = self.u - self.stepsize

        if random.uniform(0, 1) > 0.5:
            self.v = self.v + self.stepsize
        else:
            self.v = self.v - self.stepsize

        self.u = self.bind(self.u, 0, 1)
        self.v = self.bind(self.v, 0, 1)
