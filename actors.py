from vectors2d import Vector
from obstacles import Circle, Wall


class Actor:
    """The base class for all actors. Actors can move and be seen by other actors."""

    def __init__(self, simulation, position, velocity, max_speed, view_distance, view_angle, mass=1, color=(0, 0, 0)):
        self.sim = simulation

        self.pos = Vector(position[0], position[1])  # position
        self.v = Vector(velocity[0], velocity[1]).normalize() * max_speed  # velocity
        self.forces = Vector(0, 0)  # sum of all forces on the actor this frame
        self.max_speed = float(max_speed)  # the maximum speed the actor can travel at

        self.view_dist = float(view_distance)  # how far the actor can see
        self.view_angle = float(view_angle)  # in radians
        self.ahead = self.v  # look ahead vector to avoid collision

        self.mass = mass  # influences
        self.color = color  # color for display

        self.debug_avoidance = Vector(0, 0)

    def update(self, dt):
        """Updates all the actor attributes. Call this every frame after calculating all the forces."""
        self.forces += self.calc_avoidance(100)
        acceleration = self.forces / self.mass
        self.v += acceleration * dt  # update the velocity
        self.forces = Vector(0, 0)  # reset all the forces after applying them

        # Clamp the velocity at maximum speed
        if self.v.length() > self.max_speed:
            self.v = self.v.normalize() * self.max_speed

        self.pos += self.v * dt  # update the position
        self.ahead = 50 * self.v * dt  # update the ahead vector

    def calc_avoidance(self, strength):
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
                dist = self.pos.distance_to(obstacle.pos)
                if threat_dist is None or dist < threat_dist:
                    close_dist = (self.pos + small_ahead).distance_to(obstacle.pos)
                    far_dist = (self.pos + self.ahead).distance_to(obstacle.pos)
                    if close_dist <= obstacle.rad or far_dist <= obstacle.rad or dist <= obstacle.rad:
                        threat = obstacle
                        threat_dist = dist

        if type(threat) is Wall:
            avoidance = (threat.orthonormal_vector_to(self.pos)) * strength / threat_dist
            self.color = (0, 0, 255)
            self.debug_avoidance = Vector(0, 0)
            return avoidance
        elif type(threat) is Circle:
            avoidance = (self.pos - threat.pos).normalize() * strength / threat_dist
            self.debug_avoidance = avoidance
            self.color = (255, 0, 0)
            return avoidance
        else:
            self.debug_avoidance = Vector(0, 0)
            self.color = (0, 0, 0)
            return Vector(0, 0)

    def in_fov(self, point):
        """Checks if a given point is in the field of view"""
        facing_direction = self.v.normalize()
        to_point = self.pos.direction_to(point)
        return to_point.angle_to(facing_direction) <= self.view_angle / 2


class Boid(Actor):
    """Boid class."""

    def __init__(self, simulation, position, velocity, max_speed, view_distance, view_angle, mass=1, color=(0, 0, 0), flock=None):
        Actor.__init__(self, simulation, position, velocity, max_speed, view_distance, view_angle, mass, color)
        self.flock = flock  # all other boids in the simulation
        self.neighbors = []  # all boids that are close

    def update(self, dt):
        self.get_neighbors()
        self.forces += self.calc_flocking(4, 1, 1)
        Actor.update(self, dt)

    def get_neighbors(self):
        """Gets all the neighbors that are visible to the boid."""
        self.neighbors = []
        for member in self.flock:
            if member is self:
                continue
            elif self.pos.distance_to(member.pos) <= self.view_dist ** 2 and self.in_fov(member.pos):
                self.neighbors.append(member)

    def calc_flocking(self, separation_strength, alignment_strength, cohesion_strength):
        """Calculates all the flocking forces."""
        separation = self.calc_separation(separation_strength)
        alignment = self.calc_alignment(alignment_strength)
        cohesion = self.calc_cohesion(cohesion_strength)

        return separation + alignment + cohesion

    def calc_separation(self, strength, rad=20):
        """Calculate the separation force of the boids which makes them keep a minimum distance from each other."""
        if not self.neighbors:
            return Vector(0, 0)

        avg_evasion = Vector(0, 0)
        close_neighbors = 0  # the number of neighbors that are within a given separation radius

        for neighbor in self.neighbors:
            distance = self.pos.distance_to(neighbor.pos)  # distance to the neighbor
            if distance <= rad:
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
        """Calculate the alignment force of the boids which makes them align their velocity vectors."""
        if not self.neighbors:
            return Vector(0, 0)

        avg_direction = self.v.normalize()

        for neighbor in self.neighbors:
            avg_direction += neighbor.v.normalize()

        avg_direction /= len(self.neighbors) + 1  # the average direction every neighbor is facing (including self)

        alignment = avg_direction.normalize() * strength
        return alignment

    def calc_cohesion(self, strength):
        """Calculate the cohesion force of the boids which makes them stay together."""
        if not self.neighbors:
            return Vector(0, 0)

        avg_position = self.pos

        for neighbor in self.neighbors:
            avg_position += neighbor.pos

        avg_position /= len(self.neighbors) + 1  # the average position every neighbor has (including self)

        cohesion = (avg_position - self.pos).normalize() * strength
        return cohesion
