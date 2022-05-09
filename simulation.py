import numpy as np
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
                       view_distance=1,
                       view_angle=2*np.pi,
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
        # test = self.actors[0]
        # print(f"{test.v}")
        for actor in self.actors:
            actor.move(dt)  # currently, velocity is constant
            actor.get_neighbors()
            force = actor.calc_forces(2, 1, 1)
            actor.apply_force(force, dt)
            # needed for animation: actor.pos, actor.v


def main(N=50, fps=10):
    sim = Simulation()
    sim.setup(N)  # N boids (flock, no pred. currently)
    animation.main(sim, fps)


if __name__ == "__main__":
    main()
