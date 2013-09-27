import AppKit as ak

class Font(object):
    def __init__(self, name, size):
        self.font = ak.NSFont.fontWithName_size_(name, size)
        if self.font is None:
            raise ValueError('Could not create font named %s (size=%f).'%(name, size))

    def nsfont(self):
        return self.font