PyDye
======
**PyDye** is a python graphics library for OS X, powered by Apple's Quartz graphics layer.

Features
---------
- Read and write common image formats (png, jpg, tif, bmp, etc)
- Bezier paths
- Gradients
- Affine transforms
- Pixel-level access for raster graphics
- "Pythonic" API

Why?
-----
### If your target platform is Mac OS X

PyDye "just works". It has no third-party dependencies. It uses OS X's native graphics layer, so you get high quality and performance out of the box

Here are a couple of short examples of what it looks like:

#### Drawing a circle
```python
with Image(800, 600) as img:
    Oval(center=(400, 300), radius=100).fill(color=RGB(1, 0, 0))
img.save('~/Pictures/Circle.png')
```

#### Vignetting an image
```python
overlay = Gradient(start=RGBA(0, 0, 0, 0), stop=RGBA(0, 0, 0, 0.9))
with Image(path='~/Pictures/blueSky.jpg') as img:
    overlay.draw_radial_in_rect(img.bounds())
img.preview()
```

### If your target platform is not Mac OS X

See *Why Not*.

Why Not?
---------
 - It's not cross-platform - it only works on Mac OS X.
 - It's still in alpha.

Requirements
-------------
- Mac OS X 10.7 or newer

#### Dependencies already bundled with OS X
- Python 2.7
- PyObjC 