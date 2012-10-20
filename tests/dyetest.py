import unittest, os
import dye

# Global setup/teardown
session_path = None

# Testing Base Class
class DyeTestCase(unittest.TestCase):    
    def save(self, img, name):
        prefix = self.__class__.__name__.split("Test")[0]+"_"
        img.save(os.path.join(session_path, prefix+name+".png"))

# Color Constants
RED = dye.RGB(1, 0, 0)
GREEN = dye.RGB(0, 1, 0)
BLUE = dye.RGB(0, 0, 1)
BLACK = dye.RGB(0, 0, 0)

# Utility Functions
def right_arrow_path(w, h):
    m, t = w/2.0, h/3.0
    bp = dye.BezierPath()
    bp.move_to(0, t)
    bp.line_to(m, t)
    bp.line_to(m, 0)
    bp.line_to(2*m, 1.5*t)
    bp.relative_line_to(-m, 1.5*t)
    bp.relative_line_to(0, -t)
    bp.relative_line_to(-m, 0)
    bp.line_to(0, t)
    return bp
