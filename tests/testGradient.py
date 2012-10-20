from dye import Image, Gradient, Rect
from .dyetest import *

s = 200
r = Rect(0, 0, s, s)

GRAD = Gradient(start=RED, stop=BLUE)

class GradientTests(DyeTestCase):

    def test_start_stop(self):
        with Image(s, s) as img:
            Gradient(start=RED, stop=BLUE).draw_linear_in_rect(r, 90)
        self.save(img, 'Red to blue vertical linear gradient')

    def test_evenly_spaced_colors(self):
        with Image(s, s) as img:
            Gradient(colors=[RED, GREEN, BLUE]).draw_linear_in_rect(r, 0)
        self.save(img, 'RGB linear gradient')

    def test_custom_spaced_colors(self):
        with Image(s, s) as img:
            Gradient(colors={RED:0.0, GREEN:0.1, BLUE:1.0}).draw_linear_in_rect(r, 0)
        self.save(img, 'RGB with fringed red gradient')

    def test_rect_radial(self):
        with Image(s, s) as img:
            GRAD.draw_radial_in_rect(r, (0, 0))
        self.save(img, 'Radial gradient from center')

    def test_path_linear(self):
        path = right_arrow_path(s, s)
        with Image(s, s) as img:
            GRAD.draw_linear_in_path(path)
        self.save(img, 'Arrow with linear gradient')

    def test_path_radial(self):
        path = right_arrow_path(s, s)
        with Image(s, s) as img:
            GRAD.draw_radial_in_path(path)
        self.save(img, 'Arrow with radial gradient')

    def test_interpolation(self):
        self.assertEqual(GRAD.get_interpolated_color(0.0), RED)
        self.assertEqual(GRAD.get_interpolated_color(1.0), BLUE)

