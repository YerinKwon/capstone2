import math

class Coord:
    def __init__(self, x, y):
        setLocation(x, y)

    def setLocation(self, x, y):
        self.x = x
        self.y = y

    def setLocation(self, c):
        self.x = c.x
        self.y = c.y

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy

    def distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx*dx + dy*dy)

    def distance2(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx*dx + dy*dy)

    def angle(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.atan2(dy, dx)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def toString(self):
        return ("(%.2f, %.2f)", self.x, self.y)

    def clone(self):
        clone = None
        clone = super.clone()

        return clone

    def equals(self, c):
        if (c == self):
            return True
        else:
            return (self.x == c.x and self.y == c.y)

    def hashCode(self):
        return (self.x+","+self.y).hashCode()