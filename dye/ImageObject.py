import os, tempfile
from . import utils
from . import structs

class ImageObject:

    def bounds(self):
        return structs.Rect(0, 0, self.width, self.height)

    def save(self, path):
        bmp_rep = self.bitmap_representation()
        img_type = utils.get_ns_image_type(path)
        img = bmp_rep.representationUsingType_properties_(img_type, None)
        img.writeToFile_atomically_(os.path.expanduser(path), None)

    def preview(self):
        tmp = tempfile.NamedTemporaryFile(prefix='dye_', suffix='.png', delete=False)
        tmp.close()
        path = tmp.name
        self.save(path)
        os.system('open '+path)