from vectors2d import Vector
from obstacles import Circle, Wall
import math

avoidance_strength = 100.0
separation_strength = 4.0
separation_radius = 20.0
alignment_strength = 1.0
cohesion_strength = 1.0


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
        self.view_angle = float(view_angle)  # in radians
        self.ahead = self.v  # look ahead vector to avoid collision

        self.mass = mass  # influences
        self.color = color  # color for display

    def update(self, dt):
        """Updates all the actor attributes. Call this every frame after calculating all the forces."""
        self.forces += self.calc_avoidance()
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

        self.pos += self.v * dt  # update the position
        self.ahead = 50 * self.v * dt  # update the ahead vector

    def calc_avoidance(self):
        small_ahead = self.ahead / 2
        threat = None
        threat_dist = None

        for obstacle in self.sim.obstacles:
            if type(obstacle) is Wall:
                dist = obstacle.distance_to(self.pos)
                if threat_dist is None or dist < threat_dist:
                    if obstacle.intersects(self.pos, self.ahead):
                        threat = obstacle
                        threat_dist = dist
            elif type(obstacle) is Circle:
                dist = max(0.0000001, self.pos.distance_to(obstacle.pos) - obstacle.rad)
                if threat_dist is None or dist < threat_dist:
                    close_dist = (self.pos + small_ahead).distance_to(obstacle.pos)
                    far_dist = (self.pos + self.ahead).distance_to(obstacle.pos)
                    if close_dist <= obstacle.rad or far_dist <= obstacle.rad or dist <= obstacle.rad:
                        threat = obstacle
                        threat_dist = dist

        if type(threat) is Wall:
            avoidance = (threat.orthonormal_vector_to(self.pos)) * avoidance_strength / threat_dist
            return avoidance
        elif type(threat) is Circle:
            avoidance = (self.pos - threat.pos).normalize() * avoidance_strength / threat_dist
            return avoidance
        else:
            return Vector(0, 0)

    def in_fov(self, point):
        """Checks if a given point is in the field of view"""
        facing_direction = self.v.normalize()
        to_point = self.pos.direction_to(point)
        return to_point.angle_to(facing_direction) <= self.view_angle / 2


class Boid(Actor):
    """Boid class."""

    def __init__(self, simulation, position, velocity, max_speed, view_distance, view_angle, mass, color, flock, predators):
        Actor.__init__(self, simulation, position, velocity, max_speed, view_distance, view_angle, mass, color)
        self.flock = flock  # all other boids in the simulation
        self.predators = predators  # all the predators in the simulation
        self.neighbors = []  # all boids that are close
        self.threats = []  # all predators that are close (and in fov)

    def update(self, dt):
        self.get_neighbors()
        self.forces += self.calc_flocking()
        Actor.update(self, dt)

        self.change_color()

    def change_color(self):
        red_val = (1 - self.speed / self.max_speed) * 255
        self.color = (red_val, 255, 0)

    def get_neighbors(self):
        """Gets all the neighbors that are visible to the boid."""
        self.neighbors = []
        for member in self.flock:
            if member is self:
                continue
            elif self.pos.distance_to(member.pos) <= self.view_dist ** 2 and self.in_fov(member.pos):
                self.neighbors.append(member)

    def get_threats(self):
        """Gets all the predators and that are visible to the boid and classifies them as threats. Creates self.threats list."""
        self.threats = []
        for predator in self.predators:
            if self.pos.distance_to(predator.pos) <= self.view_dist ** 2:
                self.threats.apend(predator)

    def calc_flocking(self):
        """Calculates all the flocking forces."""
        separation = self.calc_separation()
        alignment = self.calc_alignment()
        cohesion = self.calc_cohesion()

        return separation + alignment + cohesion

    def calc_separation(self):
        """Calculate the separation force of the boids which makes them keep a minimum distance from each other."""
        if not self.neighbors:
            return Vector(0, 0)

        avg_evasion = Vector(0, 0)
        close_neighbors = 0  # the number of neighbors that are within a given separation radius

        for neighbor in self.neighbors:
            distance = self.pos.distance_to(neighbor.pos)  # distance to the neighbor
            if distance <= separation_radius:
                close_neighbors += 1
                # we divide by distance such the separation force is stronger for closer neighbors.
                avg_evasion += (self.pos - neighbor.pos) / distance  # vector pointing away from the neighbor

        if close_neighbors == 0:
            return Vector(0, 0)
        else:
            avg_evasion /= close_neighbors

        separation = avg_evasion.normalize() * separation_strength
        return separation

    def calc_alignment(self):
        """Calculate the alignment force of the boids which makes them align their velocity vectors."""
        if not self.neighbors:
            return Vector(0, 0)

        avg_direction = self.v.normalize()

        for neighbor in self.neighbors:
            avg_direction += neighbor.v.normalize()

        avg_direction /= len(self.neighbors) + 1  # the average direction every neighbor is facing (including self)

        alignment = avg_direction.normalize() * alignment_strength
        return alignment

    def calc_cohesion(self):
        """Calculate the cohesion force of the boids which makes them stay together."""
        if not self.neighbors:
            return Vector(0, 0)

        avg_position = self.pos

        for neighbor in self.neighbors:
            avg_position += neighbor.pos

        avg_position /= len(self.neighbors) + 1  # the average position every neighbor has (including self)

        cohesion = (avg_position - self.pos).normalize() * cohesion_strength
        return cohesion

    def calc_evasion(self):
        """Calculate the evasion force which makes them evade any predators"""
        # TODO find the closest predator
        # DONE
        closest_threat = None
        self.get_threats()
        for threat in self.threats:
            if closest_threat == None:  # dw: avoid using `is None`, weird happens
                closest_threat = threat
                continue
            elif self.pos.distance_to(threat) < self.pos.distance_to(closest_threat):
                closest_threat = threat

        # TODO calculate the evasion force (see https://gamedevelopment.tutsplus.com/tutorials/understanding-steering-behaviors-pursuit-and-evade--gamedev-2946)

        """
        vector self - threat
        future pos"""
        

        evasion = Vector(0, 0)
        return evasion


class Predator(Actor):
    """Basic predator class."""

    def __init__(self, simulation, position, velocity, max_speed, view_distance, view_angle, mass, color):
        Actor.__init__(self, simulation, position, velocity, max_speed, view_distance, view_angle, mass, color)

    def update(self, dt):
        self.forces += self.calc_pursuit()
        Actor.update(self, dt)

    def calc_pursuit(self):
        """Calculate the pursuit force which makes them pursuit the closest boid"""
        target = self.find_target()
        # TODO calculate the pursuit force (see https://gamedevelopment.tutsplus.com/tutorials/understanding-steering-behaviors-pursuit-and-evade--gamedev-2946)
        pursuit = Vector(0, 0)
        return pursuit

    def find_target(self):
        # TODO check if any boid is within view_distance
        # TODO check if any of those boids are in field of view (using self.in_fov())
        # TODO select the closest of those Boids as the new target
        target = None
        return target
