from vectors2d import Vector
from obstacles import Circle, Wall


class Actor:
    """The base class for all actors. Actors can move and be seen by other actors."""

    def __init__(self, simulation, position, velocity, speed, view_distance, view_angle):
        self.sim = simulation
        self.pos = Vector(position[0], position[1])
        self.v = Vector(velocity[0], velocity[1])
        self.speed = float(speed)
        self.view_dist = float(view_distance)  # how far the actor can see
        self.view_angle = float(view_angle)  # in radians
        self.ahead = self.pos + self.v.normalize() * self.view_dist

    def update(self, dt):
        self.pos += self.v * dt
        self.ahead = self.pos + self.v.normalize() * self.view_dist

    def apply_force(self, force, dt):
        self.v += force * dt
        # scale the velocity to the desired speed (currently constant speed)
        self.v = self.v.normalize() * self.speed

    def calc_avoidance(self, strength):
        small_ahead = self.ahead * 0.5
        threat = None
        threat_dist = self.view_dist

        for obstacle in self.sim.obstacles:
            if obstacle is Circle:
                close_dist = small_ahead.distance_sq_to(obstacle.pos)
                far_dist = self.ahead.distance_sq_to(obstacle.pos)
                if close_dist <= obstacle.rad_sq or far_dist <= obstacle.rad_sq:
                    dist = self.pos.distance_to(obstacle.pos)
                    if dist < threat_dist:
                        threat = obstacle
                        threat_dist = dist

            if obstacle is Wall:
                dist = obstacle.distance_to(self.pos)**2
                if dist < threat_dist:
                    if obstacle.intersects(self.pos, ahead):
                        threat = obstacle
                        threat_dist = dist

        if threat is Circle:
            avoidance = (self.ahead - threat.pos).normalize() * strength
            return avoidance
        elif threat is Wall:
            avoidance = (self.ahead - threat.pos).normalize() * strength
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

    def __init__(self, simulation, position, velocity, speed, view_distance, view_angle, flock):
        Actor.__init__(self, simulation, position, velocity, speed, view_distance, view_angle)
        self.neighbors = []
        self.flock = flock

    def update(self, dt):
        Actor.update(self, dt)
        self.get_neighbors()
        force = self.calc_forces(2, 1, 1, 1)
        self.apply_force(force, dt)

    def get_neighbors(self):
        """Gets all the neighbors that are visible to the boid."""
        self.neighbors = []
        for member in self.flock:
            if member is self:
                continue
            elif self.pos.distance_to(member.pos) <= self.view_dist ** 2 and self.in_fov(member.pos):
                self.neighbors.append(member)

    def calc_forces(self, separation_strength, alignment_strength, cohesion_strength, avoidance_strength):
        """Calculates all the flocking forces."""
        separation = self.calc_separation(separation_strength)
        alignment = self.calc_alignment(alignment_strength)
        cohesion = self.calc_cohesion(cohesion_strength)
        avoidance = self.calc_avoidance(avoidance_strength)

        return separation + alignment + cohesion + avoidance

    def calc_separation(self, strength, rad_sq=0.1):
        if not self.neighbors:
            return Vector(0, 0)

        avg_evasion = Vector(0, 0)
        close_neighbors = 0  # the number of neighbors that are within a given separation radius

        for neighbor in self.neighbors:
            distance = self.pos.distance_sq_to(neighbor.pos)  # distance to the neighbor
            if distance <= rad_sq:
                close_neighbors += 1
                # we divide by distance such the separation force is stronger for closer neighbors.
                avg_evasion += (self.pos - neighbor.pos) / distance  # vector pointing away from the neighbor

        if close_neighbors == 0:
            return Vector(0, 0)
        else:
            avg_evasion /= close_neighbors

        separation = avg_evasion.normalize() * strength
        return separation

    def calc_alignment(self, strength):
        if not self.neighbors:
            return Vector(0, 0)

        avg_direction = self.v.normalize()

        for neighbor in self.neighbors:
            avg_direction += neighbor.v.normalize()

        avg_direction /= len(self.neighbors) + 1  # the average direction every neighbor is facing (including self)

        alignment = avg_direction.normalize() * strength
        return alignment

    def calc_cohesion(self, strength):
        if not self.neighbors:
            return Vector(0, 0)

        avg_position = self.pos

        for neighbor in self.neighbors:
            avg_position += neighbor.pos

        avg_position /= len(self.neighbors) + 1  # the average position every neighbor has (including self)

        cohesion = (avg_position - self.pos).normalize() * strength
        return cohesion
