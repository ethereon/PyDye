import AppKit as ak
from .Color import Color

RELATIVE_CENTER = (0, 0)

class Gradient(object):

    def __init__(self, start=None, stop=None, colors=None):
        locs = None
        if start and stop:
            colors = [start, stop]
        if isinstance(colors, dict):
            colors, locs = zip(*colors.items())
        if len(colors)==0:
            raise ValueError('No gradient colors specified.')
        colors = [c.nscolor() for c in colors]
        if locs is None:
            self.gradient = ak.NSGradient.alloc().initWithColors_(colors)
        else:
            self.gradient = ak.NSGradient.alloc().initWithColors_atLocations_colorSpace_(colors,
                                                                                         locs,
                                                                                         ak.NSColorSpace.genericRGBColorSpace())

    def draw_linear_in_path(self, path, angle=0):
        self.gradient.drawInBezierPath_angle_(path.nsbezierpath(), angle)

    def draw_radial_in_path(self, path, relativeCenter=RELATIVE_CENTER):
        self.gradient.drawInBezierPath_relativeCenterPosition_(path.nsbezierpath(), relativeCenter)

    def draw_linear_in_rect(self, rect, angle=0):
        self.gradient.drawInRect_angle_(rect.nsrect(), angle)

    def draw_radial_in_rect(self, rect, relativeCenter=RELATIVE_CENTER):
        self.gradient.drawInRect_relativeCenterPosition_(rect.nsrect(), relativeCenter)

    def get_interpolated_color(self, location):
        c = self.gradient.interpolatedColorAtLocation_(location)
        return Color(c)