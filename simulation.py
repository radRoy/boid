import numpy as np
from actors import Boid
import animation


class Simulation:
    def __init__(self):
        self.actors = []  # the list to animate for each frame (see Simulation.run())

    def setup(self, nboids):
        # Create random positions and velocities
        positions = np.random.rand(nboids, 2)
        velocities = np.random.uniform(-1, 1, (nboids, 2))

        flock = []

        # Populate the actors with new boids
        for i in range(nboids):
            new = Boid(position=positions[i],
                       velocity=velocities[i],
                       speed=1,
                       view_distance=2,
                       view_angle=np.pi,
                       flock=flock)

            new.flock = flock
            flock.append(new)
            self.actors.append(new)

    def run(self, steps, dt):
        for i in range(steps):
            self.step(dt)

    def step(self, dt):
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
