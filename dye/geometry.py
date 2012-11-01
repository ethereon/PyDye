import AppKit as ak
import copy

class Rect(object):
    def __init__(self, x=None, y=None, w=None, h=None, origin=None, size=None):        
        if origin:
            self.x, self.y = origin
        else:
            self.x = x
            self.y = y
        if size:
            self.w, self.h = size
        else:
            self.w = w
            self.h = h
        assert not((self.x is None) or (self.y is None) or (self.w is None)  or (self.h is None))

    def size(self):
        return (self.w, self.h)

    def origin(self):
        return (self.x, self.y)

    def inset(self, dx, dy=None):
        r = copy.copy(self)
        dy = dy or dx
        r.x += dx
        r.y += dy
        r.w -= (2*dx)
        r.h -= (2*dy)
        return r

    def outset(self, dx, dy=None):
        dy = dy or dx
        return self.inset(-dx, -dy)

    def nsrect(self):
        return ak.NSMakeRect(self.x, self.y, self.w, self.h)

    def __str__(self):
        return 'Rect: x=%g, y=%g, width=%g, height=%g'%(self.x, self.y, self.w, self.h)

class BoundingBox(object):
    def __init__(self, min_x=None, min_y=None, max_x=None, max_y=None, points=None):
        self.min_x = min_x or float('inf')
        self.min_y = min_y or float('inf')
        self.max_x = max_x or float('-inf')
        self.max_y = max_y or float('-inf')
        if points:
            self.enclose_points(points)

    def expand(self, x, y):
        if x<self.min_x: self.min_x = x
        if x>self.max_x: self.max_x = x
        if y<self.min_y: self.min_y = y
        if y>self.max_y: self.max_y = y

    def enclose_points(self, points):
        for p in points:
            self.expand(*p)

    def rect(self):
        return Rect(self.min_x, self.min_y, self.max_x - self.min_x, self.max_y - self.min_y)

def nsrect_to_rect(r):
    return Rect(r.origin.x, r.origin.y, r.size.width, r.size.height)

def nspoint(p):
    return ak.NSMakePoint(p[0], p[1])
