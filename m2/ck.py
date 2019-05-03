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

    quiveringStates = [False, False, False, False];
    pauseStates     = [False, False, False, False];

    stepsize = 0.02;

    program = False
    data = None

    def __init__(self, data=None):

        if data == None:
            self.q1t, self.q1tRWIndex, self.q1tRWFactor, self.q1tDirection = self.initializeHelper()
            self.q2t, self.q2tRWIndex, self.q2tRWFactor, self.q2tDirection = self.initializeHelper()
            self.q3t, self.q3tRWIndex, self.q3tRWFactor, self.q3tDirection = self.initializeHelper()
            self.q4t, self.q4tRWIndex, self.q4tRWFactor, self.q4tDirection = self.initializeHelper()

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

    def initializeHelper(self): 
        qt = random.uniform(0, 1)

        maxFactor = 10
        rwIndex   = random.randint(-1, maxFactor + 1)
        rwFactor  = maxFactor
        # rwFactor  = random.randint(maxFactor-20, maxFactor)
        direction = (2 * random.randint(0,1) - 1)

        return (qt, rwIndex, rwFactor, direction)

    # Returns the appropriate direction for a quivering limb
    def quiver(self, rwIndex, rwFactor, limb_number, direction): 
        # returned_direction = direction;
        new_direction = random.uniform(0,1);

        if rwIndex < 0: 
            if random.random() > 0.66: 
                direction = -new_direction;
            else: 
                direction = new_direction;
        elif rwIndex >= rwFactor: 
            if random.random() > 0.66: 
                direction = new_direction;
            else: 
                direction = -new_direction;

        returned_direction = direction;

        return returned_direction;


    # Returns the appropriate direction for a growing limb
    def slide(self, rwIndex, rwFactor, direction): 

        if (direction == 0): 
                direction = 2 * random.randint(0,1) - 1;
                direction = direction * random.uniform(0.5,1);

        returned_direction = direction;
        new_direction = 1;

        if rwIndex < 0:         
            returned_direction = new_direction;
        elif rwIndex >= random.randint(8,200) * rwFactor: 
            returned_direction = -new_direction;

        return returned_direction;


    def pause(self): 
        self.pauseStates = [True, True, True, True];
        self.quiveringStates = [False, False, False, False];
        returned_direction = 0;
        return returned_direction;


    # Allow a quadrant to grow/shrink for a given period of time, then reevaluate whether to grow/shrink
    def stepHelper(self, qt, rwIndex, rwFactor, direction, limb_number):

        isPaused    = self.pauseStates[limb_number];
        isQuivering = self.quiveringStates[limb_number];

        # Randomize probability of pausing: 
        random_probability = random.uniform(0, 1);
        if (isPaused == False): 
            if (random_probability < 1.0 / 2000.0): 
                isPaused = True;  # Pause a moving CK w/ probability 1/300
                self.pauseStates = [True, True, True, True];
        else: 
            if (random_probability < 1.0 / 1000.0):
                # print("hello") 
                isPaused = False;  # Move a paused CK w/ probabilty 1/50
                self.pauseStates = [False, False, False, False];

        # Randomize if an arm is quivering
        if (not any(self.quiveringStates)): # if no limb is quivering
            if (random_probability < (1.0 / 50.0) * (limb_number + 1)):
                self.quiveringStates[limb_number] = True;

        # PAUSE
        if isPaused == True:
            direction = self.pause();

        # QUIVER
        elif isQuivering == True: 
            direction = self.quiver(rwIndex, rwFactor, limb_number, direction);

        # SLIDE        
        else: 
            # direction = self.quiver(rwIndex, rwFactor, direction);
            direction = self.slide(rwIndex, rwFactor, direction);
            # print("SLIDE: " + str(direction)) 

        qt = qt + (direction * self.stepsize)
        rwIndex = rwIndex + direction

        return (self.bind(qt, 0, 1), rwIndex, direction)

    def step(self):

        if self.program:
            self.q1t = self.q1t + self.stepsize*self.q1StepDirection
            self.q2t = self.q2t + self.stepsize*self.q2StepDirection
            self.q3t = self.q3t + self.stepsize*self.q3StepDirection
            self.q4t = self.q4t + self.stepsize*self.q4StepDirection

            if (abs(self.data[self.nextIdx]['q1'] - self.q1t) < 0.001 and
                abs(self.data[self.nextIdx]['q2'] - self.q2t) < 0.001 and
                abs(self.data[self.nextIdx]['q3'] - self.q3t) < 0.001 and
                abs(self.data[self.nextIdx]['q4'] - self.q4t) < 0.001):
                if len(self.data) == self.nextIdx+1:
                    return False
                else:
                    self.currentIdx = self.nextIdx
                    self.nextIdx = self.nextIdx + 1
                    self.updateStepDirection()
            return True
        else:
            self.q1t, self.q1tRWIndex, self.q1tDirection = self.stepHelper(self.q1t, self.q1tRWIndex, self.q1tRWFactor, self.q1tDirection, 0);
            self.q2t, self.q2tRWIndex, self.q2tDirection = self.stepHelper(self.q2t, self.q2tRWIndex, self.q2tRWFactor, self.q2tDirection, 1);
            self.q3t, self.q3tRWIndex, self.q3tDirection = self.stepHelper(self.q3t, self.q3tRWIndex, self.q3tRWFactor, self.q3tDirection, 2);
            self.q4t, self.q4tRWIndex, self.q4tDirection = self.stepHelper(self.q4t, self.q4tRWIndex, self.q4tRWFactor, self.q4tDirection, 3);
            return True
