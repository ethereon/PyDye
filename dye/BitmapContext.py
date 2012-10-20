import Quartz as qtz
import AppKit as ak
import os
from ImageObject import ImageObject
from Image import Image
from structs import *
from utils import *

class BitmapContext(ImageObject):

    BITS_PER_COMPONENT = 8
    BYTES_PER_PIXEL = 4

    def __init__(self, w=None, h=None, path=None):
        self.image = None
        if path is not None:
            path = os.path.expanduser(path)
            img = Image(path=path)
            self._create_context_with_size(img.width, img.height)
            with self:
                img.draw()
        elif (w and h):
            self._create_context_with_size(w, h)
        else:
            raise ValueError('Either an image path or dimensions for a new image must be provided.')

    def _create_context_with_size(self, w, h):
        self.width, self.height = w, h
        self.context = qtz.CGBitmapContextCreate(None,
                                                 w,
                                                 h,
                                                 self.BITS_PER_COMPONENT,
                                                 w*self.BYTES_PER_PIXEL,
                                                 qtz.CGColorSpaceCreateWithName(qtz.kCGColorSpaceGenericRGB),
                                                 qtz.kCGImageAlphaPremultipliedLast)
        self.data = qtz.CGBitmapContextGetData(self.context)

    def __enter__(self):
        self.context_to_restore = ak.NSGraphicsContext.currentContext()
        self.gfx_context = ak.NSGraphicsContext.graphicsContextWithGraphicsPort_flipped_(self.context, False)
        if not self.gfx_context:
            raise RuntimeError('Failed to create graphics context for bitmap context.')
        ak.NSGraphicsContext.setCurrentContext_(self.gfx_context)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.context_to_restore:
            ak.NSGraphicsContext.setCurrentContext_(self.context_to_restore)
            del self.context_to_restore

    def get_image(self):
        if self.image is None:
            self.image = qtz.CGBitmapContextCreateImage(self.context)
        return self.image

    def set_pixel(self, i, j, r, g, b, a=255):
        offset = self.BYTES_PER_PIXEL*(self.width*i+j)
        self.data[offset] = chr(r)
        self.data[offset+1] = chr(g)
        self.data[offset+2] = chr(b)
        self.data[offset+3] = chr(a)

    def get_pixel(self, i, j):
        offset = int(self.BYTES_PER_PIXEL*(self.width*i+j))
        return map(ord, (self.data[offset], self.data[offset+1], self.data[offset+2], self.data[offset+3]))

    def set_pixels(self, func):
        for i in xrange(self.width):
            for j in xrange(self.height):
                self.set_pixel(i, j, *(func(i, j)))

    def map_pixels(self, func):
        for i in xrange(self.width):
            for j in xrange(self.height):
                self.set_pixel(i, j, *(func(*(self.get_pixel(i,j)))))

    def draw(self, inRect=None):
        inRect = inRect or Rect(0, 0, self.width, self.height)
        qtz.CGContextDrawImage(current_graphics_port(), inRect.nsrect(), self.get_image())

    def bitmap_representation(self):
        return ak.NSBitmapImageRep.alloc().initWithCGImage_(self.get_image())
