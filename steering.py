from obstacles import Obstacle, Circle, Wall
from vectors2d import Vector
import math

avoidance_strength = 100.0
separation_strength = 4.0
separation_radius = 20.0
sep_rad_sq = separation_radius ** 2
alignment_strength = 1.0
cohesion_strength = 1.0
evasion_strength = 100.0
pursuit_strength = evasion_strength


def calc_avoidance(actor):
    """Calculate the avoidance force which makes the actor avoid obstacles."""
    small_ahead = actor.ahead / 2
    threat = None
    threat_dist_sq = None

    for obstacle in actor.sim.obstacles:
        if type(obstacle) is Wall:
            dist_sq = max(0.0000001, obstacle.distance_sq_to(actor.pos))
            if threat_dist_sq is None or dist_sq < threat_dist_sq:
                if obstacle.intersects(actor.pos, actor.ahead):
                    threat = obstacle
                    threat_dist_sq = dist_sq
        elif type(obstacle) is Circle:
            dist_sq = max(0.0000001, actor.pos.distance_sq_to(obstacle.pos) - obstacle.rad_sq)
            if threat_dist_sq is None or dist_sq < threat_dist_sq:
                close_dist_sq = (actor.pos + small_ahead).distance_sq_to(obstacle.pos)
                far_dist_sq = (actor.pos + actor.ahead).distance_sq_to(obstacle.pos)
                if close_dist_sq <= obstacle.rad_sq or far_dist_sq <= obstacle.rad_sq or dist_sq <= obstacle.rad_sq:
                    threat = obstacle
                    threat_dist_sq = dist_sq

    if type(threat) is Wall:
        threat_dist = math.sqrt(threat_dist_sq)
        avoidance = (threat.orthonormal_vector_to(actor.pos)) * avoidance_strength / threat_dist
        return avoidance
    elif type(threat) is Circle:
        threat_dist = math.sqrt(threat_dist_sq)
        avoidance = (actor.pos - threat.pos).normalize() * avoidance_strength / threat_dist
        return avoidance
    else:
        return Vector(0, 0)


def calc_pursuit(actor, dt, target, dist_sq):
    """Calculate the pursuit force which makes the actor pursue the target."""
    if target is None:
        return Vector(0, 0)

    dist = math.sqrt(dist_sq)
    direction = actor.pos.direction_to(target.pos + target.v * 50 * dt)
    pursuit = pursuit_strength * direction / dist

    return pursuit


def calc_evasion(actor, threat, dist_sq):
    """Calculate the evasion force which makes the actor evade the threat."""

    if threat is None:
        return Vector(0, 0)

    dist = math.sqrt(dist_sq)

    if dist <= 5.0:
        actor.sim.actors.remove(actor)
        actor.sim.flock.remove(actor)

    direction = threat.v.side(threat.pos, actor.pos) * threat.v.orthonormal()
    evasion = direction * evasion_strength / dist

    return evasion


def calc_separation(actor, neighbors):
    """Calculate the separation force of the actors which makes them keep a minimum distance from each other."""
    if not neighbors:
        return Vector(0, 0)

    avg_evasion = Vector(0, 0)
    close_neighbors = 0  # the number of neighbors that are within a given separation radius

    for neighbor in neighbors:
        dist_sq = actor.pos.distance_sq_to(neighbor.pos)  # distance to the neighbor
        if dist_sq <= sep_rad_sq:
            close_neighbors += 1
            # divide by distance such that the separation force is stronger for closer neighbors.
            avg_evasion += (actor.pos - neighbor.pos) / math.sqrt(dist_sq)  # vector pointing away from the neighbor

    if close_neighbors == 0:
        return Vector(0, 0)
    else:
        avg_evasion /= close_neighbors

    separation = avg_evasion.normalize() * separation_strength
    return separation


def calc_alignment(actor, neighbors):
    """Calculate the alignment force of the actors which makes them align their velocity vectors."""
    if not neighbors:
        return Vector(0, 0)

    avg_direction = actor.v.normalize()

    for neighbor in neighbors:
        avg_direction += neighbor.v.normalize()

    avg_direction /= len(neighbors) + 1  # the average direction every neighbor is facing (including actor)

    alignment = avg_direction.normalize() * alignment_strength
    return alignment


def calc_cohesion(actor, neighbors):
    """Calculate the cohesion force of the actors which makes them stay together."""
    if not neighbors:
        return Vector(0, 0)

    avg_position = actor.pos

    for neighbor in neighbors:
        avg_position += neighbor.pos

    avg_position /= len(neighbors) + 1  # the average position every neighbor has (including actor)

    cohesion = (avg_position - actor.pos).normalize() * cohesion_strength
    return cohesion
