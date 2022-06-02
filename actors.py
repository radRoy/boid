import random
from vectors2d import Vector
import steering


class Actor:
    """The base class for all actors. Actors can move and be seen by other actors."""

    def __init__(self, simulation, position, velocity, max_speed, view_distance, view_angle, mass, color):
        self.sim = simulation

        self.pos = Vector(position[0], position[1])  # position
        self.direction = Vector(velocity[0], velocity[1]).normalize()
        self.dir_history = [self.direction] * 10
        self.v = self.direction * max_speed  # velocity
        self.speed = max_speed
        self.forces = Vector(0, 0)  # sum of all forces on the actor this frame
        self.max_speed = float(max_speed)  # the maximum speed the actor can travel at

        self.view_dist = float(view_distance)  # how far the actor can see
        self.view_dist_sq = self.view_dist ** 2
        self.view_angle = float(view_angle)  # in radians
        self.ahead = self.v  # look ahead vector to avoid collision

        self.mass = mass  # influences
        self.color = color  # color for display

    def update(self, dt):
        """Updates all the actor attributes. Call this every frame after calculating all the forces."""

        self.forces += steering.calc_avoidance(self)
        acceleration = self.forces / self.mass

        self.v += acceleration * dt  # update the velocity

        self.speed = self.v.length()

        # Clamp the velocity at maximum speed
        if self.speed > self.max_speed:
            self.v = self.v.normalize() * self.max_speed
            self.speed = self.max_speed

        self.direction = self.v.normalize()

        del self.dir_history[0]
        self.dir_history.append(self.direction)

        self.forces = Vector(0, 0)  # reset all the forces after applying them

        if not 0 <= self.pos.x <= self.sim.window_size.x or not 0 <= self.pos.y <= self.sim.window_size.y:
            self.v = (self.sim.center - self.pos).normalize() * self.max_speed

        self.pos += self.v * dt  # update the position
        self.ahead = 50 * self.v * dt  # update the ahead vector

    def in_fov(self, point):
        """Checks if a given point is in the field of view"""
        facing_direction = self.v.normalize()
        to_point = self.pos.direction_to(point)
        return to_point.angle_to(facing_direction) <= self.view_angle / 2


class Boid(Actor):
    """Boid class."""

    def __init__(self, simulation, position, velocity, max_speed, view_distance, view_angle, mass, color):
        Actor.__init__(self, simulation, position, velocity, max_speed, view_distance, view_angle, mass, color)
        self.flock = []  # all boids of the same species
        self.neighbors = []  # all boids that are close
        self.flocking = Vector(0, 0)
        self.update_this_frame = bool(random.getrandbits(1))

    def update(self, dt):
        # only update neighbors and flocking force every second frame
        if self.update_this_frame:
            self.get_neighbors()
            self.calc_flocking()

        self.forces += self.flocking
        Actor.update(self, dt)

        self.update_this_frame = not self.update_this_frame

    def calc_flocking(self):
        """Calculates all the flocking forces."""
        separation = steering.calc_separation(self, self.neighbors)
        alignment = steering.calc_alignment(self, self.neighbors)
        cohesion = steering.calc_cohesion(self, self.neighbors)

        self.flocking = separation + alignment + cohesion

    def change_color(self):
        red_val = (1 - self.speed / self.max_speed) * 255
        self.color = (red_val, 255, 0)

    def get_neighbors(self):
        """Gets all the neighbors that are visible to the boid."""
        self.neighbors = []
        for member in self.flock:
            if member is self:
                continue
            elif self.pos.distance_sq_to(member.pos) <= self.view_dist_sq and self.in_fov(member.pos):
                self.neighbors.append(member)


class Prey(Boid):
    """Prey class."""

    def __init__(self, simulation, position, velocity, max_speed, view_distance, view_angle, mass, color):
        Boid.__init__(self, simulation, position, velocity, max_speed, view_distance, view_angle, mass, color)
        self.flock = self.sim.prey

    def update(self, dt):
        threat, threat_dist_sq = self.get_threat()
        self.forces += steering.calc_evasion(self, threat, threat_dist_sq)
        Boid.update(self, dt)

        self.change_color()

    def change_color(self):
        red_val = (1 - self.speed / self.max_speed) * 255
        self.color = (red_val, 255, 0)

    def get_threat(self):
        closest_threat = None
        closest_dist_sq = None

        for threat in self.sim.predators:
            dist_sq = self.pos.distance_sq_to(threat.pos)
            if dist_sq <= self.view_dist_sq and self.in_fov(threat.pos):
                if closest_threat is None or dist_sq < closest_dist_sq:
                    closest_threat = threat
                    closest_dist_sq = dist_sq

        return closest_threat, closest_dist_sq


class Predator(Boid):
    """Basic predator class."""

    def __init__(self, simulation, position, velocity, max_speed, view_distance, view_angle, mass, color):
        Boid.__init__(self, simulation, position, velocity, max_speed, view_distance, view_angle, mass, color)
        self.flock = self.sim.predators

    def update(self, dt):
        target, target_dist_sq = self.find_target()
        self.forces += steering.calc_pursuit(self, dt, target, target_dist_sq)
        Boid.update(self, dt)

    def find_target(self):
        """Find the nearest target"""
        closest_target = None
        closest_dist_sq = None

        for target in self.sim.prey:
            dist_sq = self.pos.distance_sq_to(target.pos)
            if dist_sq <= self.view_dist_sq and self.in_fov(target.pos):
                if closest_target is None or dist_sq < closest_dist_sq:
                    closest_target = target
                    closest_dist_sq = dist_sq

        return closest_target, closest_dist_sq
