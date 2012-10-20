import AppKit as ak

class Color(object):
    def __init__(self, color):
        self.color = color

    def nscolor(self):
        return self.color

    def set_fill(self):
        self.color.setFill()

    def set_stroke(self):
        self.color.setStroke()

    def set(self):
        self.set_fill()
        self.set_stroke()

    def fill_rect(self, rect):
        self.set_fill()
        ak.NSRectFillUsingOperation(rect.nsrect(), ak.NSCompositeSourceOver)

    @property
    def red(self):
        return self.color.redComponent()

    @property
    def green(self):
        return self.color.greenComponent()

    @property
    def blue(self):
        return self.color.blueComponent()

    @property
    def hue(self):
        return self.color.hueComponent()

    @property
    def saturation(self):
        return self.color.saturationComponent()

    @property
    def brightness(self):
        return self.color.brightnessComponent()

    def rgb(self):
        return (self.red, self.green, self.blue)

    def hsv(self):
        return (self.hue, self.saturation, self.brightness)

    def __eq__(self, other):
        return self.color.isEqual_(other.color)


class RGBA(Color):
    def __init__(self, r, g, b, a):
        self.color = ak.NSColor.colorWithCalibratedRed_green_blue_alpha_(r, g, b, a)

class RGB(RGBA):
    def __init__(self, r, g, b):
        super(RGB, self).__init__(r, g, b, 1.0)

class RGB8(RGB):
    def __init__(self, r, g, b):
        super(RGB8, self).__init__(r/255.0, g/255.0, b/255.0)

class HSVA(Color):
    def __init__(self, h, s, v, a):
        self.color = ak.NSColor.colorWithCalibratedHue_saturation_brightness_alpha_(h, s, v, a)

class HSV(HSVA):
    def __init__(self, h, s, v):
        super(HSV, self).__init__(h, s, v, 1.0)

class Gray(Color):
    def __init__(self, level):
        self.color = ak.NSColor.colorWithCalibratedWhite_alpha_(level, 1.0)