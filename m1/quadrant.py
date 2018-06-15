class Quadrant:
    def __init__(self, frm, to):
        self.frm = frm
        self.to = to

    def lerp(self, p1, p2, t):
        return ((1-t)*p1[0] + t*p2[0], (1-t)*p1[1] + t*p2[1])

    def getBezierPointsPartial(self, cval, kval, t):
        p0 = self.lerp(cval[0], kval[0], t)
        c0 = self.lerp(cval[1], kval[1], t)
        c1 = self.lerp(cval[2], kval[2], t)
        p1 = self.lerp(cval[3], kval[3], t)

        return {'p0': p0, 'c0': c0, 'c1': c1, 'p1': p1}

    def getPaths(self, t):
        paths = []
        for idx in range(len(self.frm)):
            paths.append(self.getBezierPointsPartial(self.frm[idx], self.to[idx], t))
        return paths
