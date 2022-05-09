import numpy as np
# from actors import Actor, Boid  # QU: What is module Actor needed for? TBD in future?
from actors import Boid
import animation


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


def main(N=10, fps=1):
    sim = Simulation()
    sim.setup(N)  # N boids (flock, no pred. currently)
    animation.main(sim, fps)


if __name__ == "__main__":
    main()
