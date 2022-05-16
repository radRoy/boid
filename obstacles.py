from vectors2d import Vector
import matplotlib.pyplot as plt
import math


class Obstacle:
    """The base class for all obstacles. Obstacles can be seen by actors."""

    def __init__(self, position):
        self.pos = Vector(position[0], position[1])

    def plot(self, ax):
        ax.scatter([self.pos.x], [self.pos.y])


class Circle(Obstacle):
    """A circular obstacle."""

    def __init__(self, position, radius):
        Obstacle.__init__(self, position)
        self.rad = radius
        self.rad_sq = radius ** 2


class Wall(Obstacle):
    """A straight wall"""

    def __init__(self, start, stop):
        self.start = Vector(start[0], start[1])
        self.stop = Vector(stop[0], stop[1])
        self.vector = self.stop - self.start

        self.length = (self.stop - self.start).length()

        position = (self.stop - self.start) / 2
        Obstacle.__init__(self, position)

    def determinant(self, point):
        return (self.stop.x - self.start.x) * (point.y - start.y) - (stop.y - start.y) * (point.x - start.x)

    def which_side(self, point):
        """Returns -1 if the point is on the left and +1 if it is on the right."""

        return math.copysign(1, - self.determinant(point))

    def orthonormal_vector_to(self, point):
        pass

    def distance_to(self, point):
        """Calculates the distance of the wall to a point"""

        return math.abs(self.determinant(point) / self.length)

    def intersects(self, point, vector):
        """Determines if a line given by a start point and a vector intersects the wall."""
        r = self.vector
        s = vector
        q = point
        p = self.start

        r_x_s = r.cross(s)

        if math.abs(cross1) >= 0.000001:  # if the cross product of the wall and the given vector is not zero
            t = (q - p).cross(s / r_x_s)
            u = (p - q).cross(r / (- r_x_s))
            if 0 <= t <= 1 and 0 <= u <= 1:
                return True

        return False

