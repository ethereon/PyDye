import AppKit as ak
import Quartz as qtz
from .geometry import Rect, nsrect_to_rect, nspoint
from .Color import ColorContext
from .utils import current_graphics_port
from . import AffineTransform

class BezierPath(object):

    def __init__(self, path=None):
        if path is None:
            self.path = ak.NSBezierPath.bezierPath()
        else:
            self.path = path

    def nsbezierpath(self):
        return self.path

    def quartz_path(self):
        numElements = self.path.elementCount()
        if numElements==0:
            return None
        path = qtz.CGPathCreateMutable()
        did_close_path = True
        for i in xrange(numElements):
            path_type, points = self.path.elementAtIndex_associatedPoints_(i)
            if path_type==ak.NSMoveToBezierPathElement:
                qtz.CGPathMoveToPoint(path, None, points[0].x, points[0].y)
            elif path_type==ak.NSLineToBezierPathElement:
                qtz.CGPathAddLineToPoint(path, None, points[0].x, points[0].y)
                did_close_path = False
            elif path_type==ak.NSCurveToBezierPathElement:                    
                qtz.CGPathAddCurveToPoint(path, None,
                                          points[0].x, points[0].y,
                                          points[1].x, points[1].y,
                                          points[2].x, points[2].y)
                did_close_path = False
            elif path_type==NSClosePathBezierPathElement:
                qtz.CGPathCloseSubpath(path)
                did_close_path = True
        if not did_close_path:
            qtz.CGPathCloseSubpath(path)
        immutable_path = qtz.CGPathCreateCopy(path);
        return immutable_path

    def clip_to_outline(self):
        cgpath = self.quartz_path()
        ctx = current_graphics_port()
        qtz.CGContextAddPath(ctx, cgpath)
        qtz.CGContextReplacePathWithStrokedPath(ctx)
        qtz.CGContextClip(ctx)

    def fill(self, color=None):
        with ColorContext(fill_color=color):
            self.path.fill()

    def stroke(self, color=None):
        with ColorContext(stroke_color=color):
            self.path.stroke()

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

def draw_line(p1, p2, thickness=None, color=None):    
    if thickness:
        prev_line_width = ak.NSBezierPath.defaultLineWidth()
        ak.NSBezierPath.setDefaultLineWidth_(thickness)
    with ColorContext(stroke_color=color):
        ak.NSBezierPath.strokeLineFromPoint_toPoint_(nspoint(p1), nspoint(p2))
    if thickness:
        ak.NSBezierPath.setDefaultLineWidth_(prev_line_width)
