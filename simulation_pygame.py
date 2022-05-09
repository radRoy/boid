import numpy as np
# from actors import Actor, Boid  # QU: What is module Actor needed for? TBD in future?
from actors import Boid
import pygame


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
        for i in range(steps):
            self.step(dt)
            # ani: t+=dt

    def step(self, dt):
        for actor in self.actors:
            actor.move(dt)  # currently, velocity is constant
            # needed for animation: actor.pos, actor.v



def main():
    sim = Simulation()
    sim.setup(10)
    sim.run(10, 1)


if __name__ == "__main__":
    main()
