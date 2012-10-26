import AppKit as ak
import copy

class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

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

def nsrect_to_rect(r):
    return Rect(r.origin.x, r.origin.y, r.size.width, r.size.height)

def nspoint(p):
    return ak.NSMakePoint(p[0], p[1])