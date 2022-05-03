import math


class Vector(tuple):
    """A 2D vector"""

    def __new__(cls, x, y):
        # Vectors inherit from the tuple.
        return tuple.__new__(Vector, (x, y))

    def __init__(self, x, y):
        self.x = float(x)  # x coordinate
        self.y = float(y)  # y coordinate

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other)
        else:
            # Multiplication turns into dot product if the other object is also a Vector
            return self.dot(other)

    def length_sq(self):
        """Returns the squared length (magnitude) of the vector."""
        return (self.x * self.x) + (self.y * self.y)

    def length(self):
        """Returns the length (magnitude) of the vector."""
        return math.sqrt(self.length_sq())

    def inverse(self):
        """Returns the inverse of the vector."""
        return Vector(1.0 / self.x, 1.0 / self.y)

    def normalize(self):
        """Returns the normalized vector such that it's length is 1 but direction stays the same."""
        length = self.length()
        if length == 0.0:
            return Vector(0, 0)
        return Vector(self.x / length, self.y / length)

    def dot(self, other):
        """Returns the dot product of the vector and a given second vector."""
        return self.x * other.x + self.y * other.y

    def direction_to(self, point):
        """Returns a normalized vector that points into the direction of a given point."""
        return (point - self).normalize()

    def distance_sq_to(self, point):
        """Returns the distance squared to a given point."""
        return abs(self.x - point.x) ** 2 + abs(self.y - point.y) ** 2

    def distance_to(self, point):
        """Returns the distance to a given point."""
        return math.sqrt(self.distance_sq_to(point))

    def angle_to(self, point):
        """Returns the smallest, unsigned angle to a given point."""
        dot_prod = self.normalize().dot(point.normalize)
        return math.acos(dot_prod)
