
# What?
This is a monkey patcher for `fontParts` and `defcon` objects. It's one way of adding more high level functions to these packages without having to modify their code directly.

# Usage
Add your own methods to fontpart/defcon objects by simply defining a fuction. The first argument of the function should be a defcon object, like `font`, `glyph`, etc. Before the function use the one of the decorators from this package: `fontMethod` or `fontCached` method.

## Exmaples
Define a new method for glyph object:
```py
from fontGadgets.tools import fontMethod

@fontMethod
def isEmpty(glyph):
    return glyph.contours == () and glyph.anchors == () and glyph.components == ()
```

Now glyph object has a new property. Because the function that was define had only one argument, the `glyph` object:
```
>>> glyph.isEmpty
True
```

You can also define a method that can be more efficent if the code is performance heavy. Note that the argument types should be immutable (e.g. int, str, etc.):
```py
from fontGadgets.tools import fontCachedMethod
from drawBot import BezierPath
from defcon import Glyph
from fontTools.pens.cocoaPen import CocoaPen

@fontCachedMethod("Glyph.ContoursChanged", "Glyph.ComponentsChanged", "Component.BaseGlyphChanged")
def getStroked(glyph, strokeWidth):
    """
    Returns a stroked copy of the glyph with the defined stroked width. The `strokeWidth` is an integer.
    """
    print('One more time')
    pen = CocoaPen(glyph.font)
    glyph.draw(pen)
    bezierPath = BezierPath(pen.path)
    bezierPath.removeOverlap()
    newPath = bezierPath.expandStroke(strokeWidth).removeOverlap()
    union = newPath.union(bezierPath)
    result = Glyph()
    p = result.getPen()
    union.drawToPen(p)
    return result

g = CurrentGlyph()
g.getStroked(10)
```
This new method will only be executed if any the destructive notification inside the `fontCachedMethod` have been called on the glyph object. This makes it faster to fetch the result if you 
want to call it over and over.


# Warning
This is WIP, use it at your own risk!