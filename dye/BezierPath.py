import AppKit as ak
from utils import *
from structs import *
import AffineTransform

class BezierPath(object):

    def __init__(self, path=None):
        if path is None:
            self.path = ak.NSBezierPath.bezierPath()
        else:
            self.path = path

    def nsbezierpath(self):
        return self.path
            
    def fill(self, color=None):
        perform_op_with_color(self.path.fill, fill_color=color)

    def stroke(self, color=None):
        perform_op_with_color(self.path.stroke, stroke_color=color)

    def fill_stroke(self, fill_color=None, stroke_color=None):
        self.fill(fill_color)
        self.stroke(stroke_color)

    def add_clip(self):
        self.path.addClip()

    def set_clip(self):
        self.path.setClip()

    def move_to(self, x, y):
        self.path.moveToPoint_((x, y))

    def line_to(self, x, y):
        self.path.lineToPoint_((x, y))

    def relative_move_to(self, x, y):
        self.path.relativeMoveToPoint_((x, y))

    def relative_line_to(self, x, y):
        self.path.relativeLineToPoint_((x, y))

    def set_line_width(self, w):
        self.path.setLineWidth_(w)

    def apply_transform(self, xform):
        self.path.transformUsingAffineTransform_(xform.transform)

    def line_width(self):
        return self.path.lineWidth()

    def bounds(self, stroked=True):        
        b = nsrect_to_rect(self.path.bounds())
        # Adjust for line width
        return b.outset(self.line_width()) if stroked else b

    def normalize_origin(self, stroked):
        b = self.bounds(stroked=stroked)
        self.apply_transform(AffineTransform.translation(-b.x, -b.y))

class Rectangle(BezierPath):

    def __init__(self, rect):
        path = ak.NSBezierPath.bezierPathWithRect_(rect.nsrect())
        super(Rectangle, self).__init__(path)

class RoundedRectangle(BezierPath):

    def __init__(self, rect, x_radius, y_radius=None):
        y_radius = y_radius or x_radius
        path = ak.NSBezierPath.bezierPathWithRoundedRect_xRadius_yRadius_(rect.nsrect(), x_radius, y_radius)
        super(RoundedRectangle, self).__init__(path)

class Oval(BezierPath):

    def __init__(self, rect=None, radius=None, center=None):
        if (radius and center):
            rect = Rect(center[0]-radius, center[1]-radius, 2*radius, 2*radius)
        if rect is None:
            raise ValueError("Parameters for establishing the oval's bounding rect not specified.")
        path = ak.NSBezierPath.bezierPathWithOvalInRect_(rect.nsrect())
        super(Oval, self).__init__(path)