import AppKit as ak
from geometry import nspoint

class TextAttributes(object):
    def __init__(self, font, color):
        self.font = font
        self.color = color

    def attributes_dict(self):
        return {ak.NSFontAttributeName: self.font.nsfont(),
                ak.NSForegroundColorAttributeName: self.color.nscolor()}

    def attributed_string(self, text):
        return ak.NSAttributedString.alloc().initWithString_attributes_(text, self.attributes_dict())

    def draw_text(self, text, rect=None, point=None):
        attr_s = self.attributed_string(text)
        if rect is not None:
            attr_s.drawInRect_(rect.nsrect())
        elif point is not None:
            attr_s.drawAtPoint_(nspoint(point))
        else:
            raise ValueError("Either rect or point must be specified.")

    def size_of_text(self, text):
        return self.attributed_string(text).size()

