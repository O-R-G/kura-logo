from quadrant import Quadrant
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

    # q1 - top right
    q1from = [
        [(566.4, 424.9), (523.2,499.6), (442.4,549.8), (350,549.8)],
        [(350, 549.8), (212,549.8), (100.2,438), (100.45,300)]
    ]
    q1to = [
        [(350.5,549.8), (288.05,487.35), (288.05,487.35), (225.6,424.9)],
        [(225.6,424.9), (163.15,362.45), (163.15,362.5), (100.45,300)]
    ]

    # q2 - top left
    q2from = [
        [(35.7,50.2), (35.7,175.1), (35.7,175.1), (35.7,300)]
    ]

    q2to = [
        [(35.7,300), (35.7,300), (35.7,300), (35.7,300)]
    ]

    # q3 - bottom left
    q3from = [
        [(35.7,300), (35.7,424.9), (35.7,424.9), (35.7,549.8)]
    ]

    q3to = [
        [(35.7,300), (35.7,300), (35.7,300), (35.7,300)]
    ]

    # q4 - bottom right
    q4from = [
        [(100.45, 300), (100.2,162), (212,50.2), (350,50.2)],
        [(350,50.2), (442.4,50.2), (523.2,100.4), (566.4,175.1)]
    ]
    q4to = [
        [(100.45,300), (163.15,237.55), (163.15,237.55), (225.6,175.1)],
        [(225.6,175.1), (288.05,112.65), (288.05,112.65), (350.5,50.2)]
    ]

    stepsize = 0.02

    program = False
    data = None

    def __init__(self, data=None):
        if data == None:
            self.q1t = random.uniform(0, 1)
            self.q2t = random.uniform(0, 1)
            self.q3t = random.uniform(0, 1)
            self.q4t = random.uniform(0, 1)
        else:
            self.program = True
            self.data = data
            self.currentIdx = 0
            self.nextIdx = 1
            self.q1t = self.data[self.currentIdx]['q1']
            self.q2t = self.data[self.currentIdx]['q2']
            self.q3t = self.data[self.currentIdx]['q3']
            self.q4t = self.data[self.currentIdx]['q4']

            self.updateStepDirection()

        self.q1 = Quadrant(self.q1from, self.q1to)
        self.q2 = Quadrant(self.q2from, self.q2to)
        self.q3 = Quadrant(self.q3from, self.q3to)
        self.q4 = Quadrant(self.q4from, self.q4to)

    def updateStepDirection(self):
        self.q1StepDirection = self.data[self.nextIdx]['q1'] - self.data[self.currentIdx]['q1']
        self.q2StepDirection = self.data[self.nextIdx]['q2'] - self.data[self.currentIdx]['q2']
        self.q3StepDirection = self.data[self.nextIdx]['q3'] - self.data[self.currentIdx]['q3']
        self.q4StepDirection = self.data[self.nextIdx]['q4'] - self.data[self.currentIdx]['q4']

    def getPaths(self):
        return {
            'q1': self.q1.getPaths(self.q1t),
            'q2': self.q2.getPaths(self.q2t),
            'q3': self.q3.getPaths(self.q3t),
            'q4': self.q4.getPaths(self.q4t),
        }

    def bind(self, value, lower, upper):
        if value < lower:
            return lower
        if value > upper:
            return upper
        return value

    def stepHelper(self, qt):
        if random.uniform(0, 1) > 0.5:
            qt = qt + self.stepsize
        else:
            qt = qt - self.stepsize

        return self.bind(qt, 0, 1)

    def step(self):
        if self.program:
            self.q1t = self.q1t + self.stepsize*self.q1StepDirection
            self.q2t = self.q2t + self.stepsize*self.q2StepDirection
            self.q3t = self.q3t + self.stepsize*self.q3StepDirection
            self.q4t = self.q4t + self.stepsize*self.q4StepDirection

            if (abs(self.data[self.nextIdx]['q1']-self.q1t) < .001 and
            abs(self.data[self.nextIdx]['q2']-self.q2t) < .001 and
            abs(self.data[self.nextIdx]['q3']-self.q3t) < .001 and
            abs(self.data[self.nextIdx]['q4']-self.q4t) < .001):
                if len(self.data) == self.nextIdx+1:
                    return False
                else:
                    self.currentIdx = self.nextIdx
                    self.nextIdx = self.nextIdx +1
                    self.updateStepDirection()
            return True
        else:
            self.q1t = self.stepHelper(self.q1t)
            self.q2t = self.stepHelper(self.q2t)
            self.q3t = self.stepHelper(self.q3t)
            self.q4t = self.stepHelper(self.q4t)
            return True
