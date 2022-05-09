import numpy as np
# from actors import Actor, Boid  # QU: What is module Actor needed for? TBD in future?
from actors import Boid
#from itertools import count
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

    dt_main = fps/1000
    ani = FuncAnimation(plt.gcf(), animate, fargs=(Sim, dt_main,), interval=dt_main)

    plt.tight_layout()
    ani.save("boids.gif", writer="pillow")


if __name__ == "__main__":
    print("main namespace")
    main(100, 10)
    print("main() done.")
