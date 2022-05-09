import numpy as np
# from actors import Actor, Boid  # QU: What is module Actor needed for? TBD in future?

# from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def animate(i, ani, dt_animate):
    boids = ani.actors

    plt.clf()  # clear axis, if axis should change

    for boid in boids:
        xp = boid.pos[0]
        yp = boid.pos[1]
        # xv = boid.v[0]
        # yv = boid.v[1]

        plt.scatter(xp, yp, c="black")
        # could also first create one np.array of all boids and call plt.plot() once for whole array

    plt.tight_layout()

    ani.run(1, dt_animate)


def main(Sim, fps):

    dt_main = 1/fps
    ani = FuncAnimation(plt.gcf(), animate, frames=200, fargs=(Sim, dt_main,), interval=dt_main)

    plt.tight_layout()
    ani.save("boids.gif", writer="pillow")
