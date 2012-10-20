#!/usr/bin/env python

import dye
import unittest, os
from .dyetest import *

class BezierPathTests(DyeTestCase):

    def test_fill_stroke(self):
        w, h = 200, 200
        line_width = 4
        img = dye.Image(w, h)
        bp = dye.Oval(rect=img.bounds().inset(line_width))
        bp.set_line_width(line_width)
        self.assertEqual(bp.line_width(), line_width)
        with img:
            RED.set_fill()
            bp.fill()
            BLUE.set_stroke()
            bp.stroke()
        self.save(img, 'Circle with red fill and blue stroke')

    def test_line(self):
        bp = right_arrow_path(600, 600)
        r = bp.bounds(stroked=False)
        with dye.Image(r.w, r.h) as img:
            bp.fill(color=RED)
        self.save(img, 'Red arrow pointing right')

    def test_clipping(self):
        img_rect = dye.Rect(0, 0, 200, 200)
        square = dye.Rectangle(img_rect.inset(30))
        circle = dye.Oval(img_rect.inset(20))
        circle.set_line_width(4)
        with dye.Image(img_rect.w, img_rect.h) as img:
            circle.stroke(color=BLACK)
            circle.set_clip()
            square.fill(color=RED)
        self.save(img, 'Square clipped by a circle')

    def test_normalize_origin(self):
        s = 200
        circle = dye.Oval(dye.Rect(10, 10, s, s))
        circle.normalize_origin(stroked=False)
        with dye.Image(s, s) as img:
            BLACK.fill_rect(dye.Rect(0, 0, s, s))
            circle.fill(RED)
        self.save(img, 'Perfectly fitting circle')

    def test_rounded_rect(self):
        with dye.Image(200, 200) as img:
            dye.RoundedRectangle(dye.Rect(20, 20, 160, 160), 10).fill(RED)
        self.save(img, 'Rounded Rectangle')      

    def test_relative_oval(self):
        with dye.Image(200, 200) as img:
            dye.Oval(center=(100, 100), radius=50).fill(color=dye.RGB(1, 0, 0))
        self.save(img, 'Centered circle of radius 50')