import AppKit as ak
import Quartz as qtz
import os
from .ImageObject import ImageObject

class Image(ImageObject):

    def __init__(self, w=None, h=None, path=None, unprepared=False):
        if path is not None:
            path = os.path.expanduser(path)
            img = ak.NSImage.alloc().initWithContentsOfFile_(path)
            if not img:
                raise ValueError('Could not create image from file at %s'%path)
            self.set_internal_image(img)
        elif (w and h):
            self.set_internal_image(ak.NSImage.alloc().initWithSize_((w, h)))
        elif not unprepared:
            raise ValueError('Either an image path or dimensions for a new image must be provided.')

    def set_internal_image(self, img):
        assert img.isKindOfClass_(ak.NSImage.class__())
        self.img = img
        img_size = self.img.size()
        self.width, self.height = img_size.width, img_size.height

    def draw(self, x=0, y=0, w=None, h=None):
        w, h = w or self.width, h or self.height
        self.img.drawInRect_fromRect_operation_fraction_respectFlipped_hints_(ak.NSMakeRect(x, y, w, h),
                                                                              ak.NSZeroRect,
                                                                              ak.NSCompositeSourceOver,
                                                                              1.0,
                                                                              True,
                                                                              None)

    def bitmap_representation(self):
        return ak.NSBitmapImageRep.imageRepWithData_(self.img.TIFFRepresentation())

    def __enter__(self):
        self.img.lockFocus()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.img.unlockFocus()

    def color_masked(self, color):
        img_size = ak.NSMakeSize(self.width, self.height)
        masked_img = self.img.copy()
        masked_img.lockFocus()
        color.set_fill()
        ak.NSRectFillUsingOperation(ak.NSMakeRect(0, 0, self.width, self.height), ak.NSCompositeSourceAtop)
        masked_img.unlockFocus()
        img_out = Image(unprepared=True)
        img_out.set_internal_image(masked_img)
        return img_out
