from generator import Generator
from viewer import Viewer
import random

def bind(value, lower, upper):
    if value < lower:
        return lower
    if value > upper:
        return upper
    return value

def main():
    # run
    steps = 50
    stepsize = 0.02
    u = random.uniform(0, 1)
    v = random.uniform(0, 1)
    w = random.uniform(1, 100)
    # w = 66

    generator = Generator()
    for t in range(0, steps+1):
        generator.generate(u, v, w)
        generator.save('run/' + str(t) + '.svg')
        viewer.openFile('run/' + str(t) + '.svg')

        if random.uniform(0, 1) > 0.5:
            u = u + stepsize
        else:
            u = u - stepsize

        if random.uniform(0, 1) > 0.5:
            v = v + stepsize
        else:
            v = v - stepsize

        if random.uniform(0, 1) > 0.5:
            w = w + 5
        else:
            w = w - 5

        u = bind(u, 0, 1)
        v = bind(v, 0, 1)
        w = bind(w, 1, 100)

if __name__ == "__main__":
    main()
