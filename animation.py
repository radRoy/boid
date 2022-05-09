import numpy as np
# from actors import Actor, Boid  # QU: What is module Actor needed for? TBD in future?
from actors import Boid
#from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Simulation:
    def __init__(self):
        self.actors = []  # the list to animate for each frame (see Simulation.run())

    def setup(self, nboids):
        # Create random positions and velocities
        positions = np.random.rand(nboids, 2)
        velocities = np.random.rand(nboids, 2)

        flock = []

        # Populate the actors with new boids
        for i in range(nboids):
            new = Boid(position=positions[i],
                       velocity=velocities[i],
                       speed=1,
                       view_distance=2,
                       view_angle=2 * np.pi,
                       flock=flock)

            # QU: Is new.flock an alias of flock?
            # (= will new.flock be updated when another Boid() joins the flock?)
            new.flock = flock
            flock.append(new)
            self.actors.append(new)

    def run(self, steps, dt):
        # ani: t=0
        for i in range(steps):  # ani: change to while True loop? break if window closed?
            self.step(dt)
            # ani: t+=dt

    def step(self, dt):
        for actor in self.actors:
            actor.move(dt)  # currently, velocity is constant
            # needed for animation: actor.pos, actor.v


def animate(i, ani, dt_animate):
    ani: Simulation
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
