import AppKit as ak
import Quartz as qtz
import os, tempfile

EXT_TO_IMG_TYPE_TABLE = { 'png':ak.NSPNGFileType,
                          'jpg':ak.NSJPEGFileType,
                          'jpeg':ak.NSJPEGFileType,
                          'tif':ak.NSTIFFFileType,
                          'tiff':ak.NSTIFFFileType,
                          'bmp':ak.NSBMPFileType,
                          'giff':ak.NSGIFFileType,
                          'gif':ak.NSGIFFileType, }

def current_graphics_context():
    return ak.NSGraphicsContext.currentContext()

def current_graphics_port():
    return current_graphics_context().graphicsPort()

def get_ns_image_type(filename, typeName=None):
    if typeName is None:
        ext = os.path.splitext(filename)[1]
        if len(ext)>1:
            typeName = ext[1:]
    imgType = EXT_TO_IMG_TYPE_TABLE.get(typeName)
    if imgType is None:
        raise ValueError('Unsupported image type requested')
    return imgType

def save_graphics_state():
    ak.NSGraphicsContext.saveGraphicsState()

def restore_graphics_state():
    ak.NSGraphicsContext.restoreGraphicsState()

def perform_op_with_color(func, fill_color=None, stroke_color=None):
    if (fill_color is None ) and (stroke_color is None):
        func()
    else:
        save_graphics_state()
        if fill_color is not None:
            fill_color.set_fill()
        if stroke_color is not None:
            stroke_color.set_stroke()
        func()
        restore_graphics_state()