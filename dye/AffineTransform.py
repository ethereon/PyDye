import AppKit as ak

class AffineTransform:
    def __init__(self):
        self.transform = ak.NSAffineTransform.transform()

    def rotate_degrees(self, degs):
        self.transform.rotateByDegrees_(degs)

    def rotate_radians(self, rads):
        self.transform.rotateByRadians(rads)

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

    def apply(self, x, y):
        p = self.transform.transformPoint((x, y))
        return (p.x, p.y)

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