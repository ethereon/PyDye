import dye
import math, colorsys
from .dyetest import *

class BitmapContextTests(DyeTestCase):

    def test_render_color_wheel(self):
        WHEEL_RADIUS = 200        
        def color_at_location(i, j):
            x, y = j - WHEEL_RADIUS, WHEEL_RADIUS - i
            theta = math.atan2(y, x)
            if (theta<0): theta += (2*math.pi)
            sat = min(1.0, math.sqrt((x*x)+(y*y))/WHEEL_RADIUS)
            return (int(v*255) for v in colorsys.hsv_to_rgb(theta/(2*math.pi), sat, 1.0))
        dia = 2*WHEEL_RADIUS
        bitmap = dye.BitmapContext(dia, dia)
        bitmap.set_pixels(color_at_location)
        img = dye.Image(dia, dia)
        with img:
            dye.Oval(dye.Rect(0, 0, dia, dia)).set_clip()
            bitmap.draw()
        self.save(img, "Color Wheel")