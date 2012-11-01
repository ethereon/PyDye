import AppKit as ak

class AffineTransform:
    def __init__(self, transform=None):
        if transform is None:
            self.transform = ak.NSAffineTransform.transform()
        else:
            self.transform = ak.NSAffineTransform.alloc().initWithTransform_(transform.nstransform())

    def nstransform(self):
        return self.transform

    def rotate_degrees(self, degs):
        self.transform.rotateByDegrees_(degs)

    def rotate_radians(self, rads):
        self.transform.rotateByRadians_(rads)

    def scale(self, scaleX, scaleY=None):
        if scaleY is None:
            scaleY = scaleX
        self.transform.scaleXBy_yBy_(scaleX, scaleY)

    def translate(self, dX, dY):
        self.transform.translateXBy_yBy_(dX, dY)

    def append_transform(self, xform):
        self.transform.appendTransform_(xform.transform)

    def prepend_transform(self, xform):
        self.transform.prependTransform_(xform.transform)

    def invert(self):
        self.transform.invert()

    def transform_point(self, x, y):
        p = self.transform.transformPoint((x, y))
        return (p.x, p.y)

    def concat(self):
        self.transform.concat()

    def __enter__(self):
        self.concat()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        inverse_xform = AffineTransform(transform=self)
        inverse_xform.invert()
        inverse_xform.concat()

def translation(dx, dy):
    xform = AffineTransform()
    xform.translate(dx, dy)
    return xform

def scaling(sx, sy):
    xform = AffineTransform()
    xform.scale(sx, sy)
    return xform

def rotation(degrees):
    xform = AffineTransform()
    xform.rotate_degrees(degrees)
    return xform