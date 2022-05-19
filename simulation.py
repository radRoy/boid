import numpy as np
from actors import Boid
from obstacles import Obstacle, Circle, Wall
from vectors2d import Vector


class Simulation:
    def __init__(self, window_size=(1, 1)):
        self.window_size = Vector(window_size[0], window_size[1])
        self.actors = []
        self.obstacles = []
        self.boid_settings = {"max_speed": 0.1, "view_distance": 50, "view_angle": np.pi, "mass": 5000, "color": (0, 0, 0)}

    def setup(self, nboids):
        # Create random positions and velocities
        x_vals = np.random.uniform(0, self.window_size[0], nboids)
        y_vals = np.random.uniform(0, self.window_size[1], nboids)
        positions = np.column_stack((x_vals, y_vals))
        velocities = np.random.uniform(-1, 1, (nboids, 2))

        # Create four walls around the edges
        top_wall = Wall((0, 0), (self.window_size[0], 0))
        right_wall = Wall((self.window_size[0], 0), (self.window_size[0], self.window_size[1]))
        bottom_wall = Wall((self.window_size[0], self.window_size[1]), (0, self.window_size[1]))
        left_wall = Wall((0, self.window_size[1]), (0, 0))

        self.obstacles.extend([top_wall, right_wall, bottom_wall, left_wall])

        flock = []
        # Populate the actors with new boids
        for i in range(nboids):
            new = Boid(simulation=self,
                       position=positions[i],
                       velocity=velocities[i],
                       max_speed=self.boid_settings["max_speed"],
                       view_distance=self.boid_settings["view_distance"],
                       view_angle=self.boid_settings["view_angle"],
                       mass=self.boid_settings["mass"],
                       color=self.boid_settings["color"],
                       flock=flock)

            flock.append(new)
            self.actors.append(new)

    def run(self, steps, dt):
        for i in range(steps):
            self.step(dt)

    def step(self, dt):
        for actor in self.actors:
            actor.update(dt)


def main():
    sim = Simulation()
    sim.setup(10)
    sim.run(100, 1)


if __name__ == "__main__":
    main()
