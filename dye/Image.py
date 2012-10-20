import AppKit as ak
import Quartz as qtz
import os
from ImageObject import ImageObject

class Image(ImageObject):
    
    def __init__(self, w=None, h=None, path=None):        
        if path is not None:
            path = os.path.expanduser(path)
            self.img = ak.NSImage.alloc().initWithContentsOfFile_(path)
            if not self.img:
                raise ValueError('Could not create image from file at %s'%path)
            img_size = self.img.size()
            self.width, self.height = img_size.width, img_size.height
        elif (w and h):
            self.width = w
            self.height = h
            self.img = ak.NSImage.alloc().initWithSize_((w, h))
        else:
            raise ValueError('Either an image path or dimensions for a new image must be provided.')

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
