import dye
from .dyetest import *

class BitmapContextTests(DyeTestCase):

    def test_color_masking(self):
        bp = right_arrow_path(600, 600)
        r = bp.bounds(stroked=False)
        with dye.Image(r.w, r.h) as img:
            bp.fill(color=RED)
        self.save(img.color_masked(color=GREEN), 'Green right arrow')
