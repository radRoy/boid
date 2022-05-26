import numpy as np
from actors import Boid
from obstacles import Obstacle, Circle, Wall
from vectors2d import Vector


class Simulation:
    def __init__(self, window_size=(1, 1)):
        self.window_size = Vector(window_size[0], window_size[1])
        self.actors = []
        self.obstacles = []
        self.boid_settings = {"max_speed": 0.1, "view_distance": 50, "view_angle": np.pi, "mass": 5000,
                              "color": (0, 0, 0)}

    def setup(self, nboids):
        # Create four walls around the edges and add them to the obstacles
        top_wall = Wall((0, 0), (self.window_size[0], 0))
        right_wall = Wall((self.window_size[0], 0), (self.window_size[0], self.window_size[1]))
        bottom_wall = Wall((self.window_size[0], self.window_size[1]), (0, self.window_size[1]))
        left_wall = Wall((0, self.window_size[1]), (0, 0))
        self.add_obstacles(top_wall, right_wall, bottom_wall, left_wall)

        # Create random positions and velocities
        x_vals = np.random.uniform(0, self.window_size[0], nboids)
        y_vals = np.random.uniform(0, self.window_size[1], nboids)
        positions = np.column_stack((x_vals, y_vals))
        velocities = np.random.uniform(-1, 1, (nboids, 2))

        # Populate the actors with new boids
        flock = []
        self.add_n_boids(nboids, flock, positions, velocities)

    def add_obstacles(self, *args):
        for obstacle in args:
            self.obstacles.append(obstacle)

    def delete_obstacles(self, *args):
        for obstacle in args:
            self.obstacles.remove(obstacle)
            del obstacle

    def add_n_boids(self, n, flock, positions, velocities):
        for i in range(n):
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

    def step(self, dt):
        for actor in self.actors:
            actor.update(dt)
