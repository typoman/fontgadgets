# FontGadgets

[License](https://github.com/typoman/fontgadgets/blob/main/LICENSE)

A library that extends the capabilities of `defcon` and `FontParts` objects with high-level methods.
## Why?
Are you tired of writing or copying the same function for every font project? FontGadgets centralizes common, high-level font manipulation tasks by attaching them directly to the defcon and FontParts objects you already use. This keeps your scripts cleaner and your workflow more organized. I also created tools for working with complex fonts and some of these tools share the same functionalities. So I decided to put everything in one place.
## What is FontGadgets?
FontGadgets is a Python package that uses a technique called "monkey patching" to add new functionalities or "extensions" to the core objects of `defcon` and `FontParts`. This approach allows addition of these new methods without modifying the original source code of these libraries. I see it myself as my playground for extending their capabilites before proposing new ideas or additions.
## Installation
To install the latest version from the repository in editable mode, follow these steps:

```bash
git clone https://github.com/typoman/fontgadgets
cd fontgadgets
pip3 install -e .
```
## Adding Your Own Extensions
You can easily add your own methods to `defcon` and `FontParts` objects using the decorators provided by FontGadgets. The first argument of your function should always be an instance of the object you intend to modify (e.g., `font`, `glyph`).
### Available Decorators
*   `@font_method`: Adds a regular method to a class.
*   `@font_property`: Adds a read-only dynamic attribute (a property) to a class.
*   `@font_property_setter`: Adds a setter for an existing property.
*   `@font_cached_method`: Adds a method whose results are cached. The cache is invalidated based on the destructive notifications which belong to the object you add the method to. For example for finding the glyph object destructive notifications you can run `help(defcon.Glyph)`.
*   `@font_cached_property`: Adds a cached property. You also need to pass the destructive notificationts list as the argument of the decorator just like the `font_cached_method`.
### Examples
#### Adding a Dynamic Attribute
Here's how to add an `isComposite` property to a glyph object, which will be `True` if the glyph is a composite.
```python
from fontgadgets.decorators import font_property

@font_property
def isComposite(glyph):
    """
    Returns True if the glyph is a composite, False otherwise.
    """
    return len(glyph.contours) == 0 and len(glyph.components) > 0
```
Now, you can access this as a property on any glyph object:
```python
>>> myGlyph.isComposite
True
```
#### Adding a Cached Method
For performance-heavy operations, you can use a cached method. The following example creates a stroked version of a glyph. The result is cached and will only be re-calculated if the glyph's contours or components change.
```python
from fontgadgets.decorators import font_cached_method
from drawBot import BezierPath
from defcon import Glyph
from fontTools.pens.cocoaPen import CocoaPen

@font_cached_method("Glyph.ContoursChanged", "Glyph.ComponentsChanged", "Component.BaseGlyphChanged") # You can find the list of notifications from each defcon object by using for example, help(defcon.Glyph)
def getStroked(glyph, strokeWidth):
    """
    Returns a stroked copy of the glyph with the defined stroke width.
    """
    print("Executing the stroking logic...")
    pen = CocoaPen(glyph.font)
    glyph.draw(pen)
    bezierPath = BezierPath(pen.path)
    bezierPath.removeOverlap()
    newPath = bezierPath.expandStroke(strokeWidth).removeOverlap()
    union = newPath.union(bezierPath)
    result = Glyph()
    pen = result.getPen()
    union.drawToPen(pen)
    return result

# To ensure the cache persists, run this code from a separate module/file:
g = font['a']
g.getStroked(10)

# "Executing the stroking logic..." is printed

g.getStroked(10)
# The message is not printed because the cached result is returned instantly and the function body is not executed.
```
### Advanced Usage: Type Hinting
You can control which library (`defcon` or `FontParts`) a method is added to by using Python's type hints.
#### Targeting a Specific Object
To add a method exclusively to a `fontParts.fontshell.RSegment` object (`defcon` doesn't have a segment object), you can do the following:
```python
from fontgadgets.decorators import font_method
from fontParts.fontshell import RSegment

@font_method
def myFunction(segment: RSegment):
    # This logic will only be available on RSegment objects
    pass
```
#### Controlling the Return Types
If your method returns a `defcon` object, FontGadgets can automatically wrap it in the corresponding `FontParts` object when the method is called from a `FontParts` instance. You just need to add the return type hint to the function definition.
```python
from fontgadgets.decorators import font_method
import defcon

@font_method
def subset(font) -> defcon.Font: # Note the return type hint
    # ... subsetting logic that returns a new defcon.Font
    return new_defcon_font
```
When you call `my_rfont_object.subset()` on a `RFont` object, the returned `defcon.Font` will be automatically converted to a `fontParts.fontshell.RFont` object.
## Available Extensions
FontGadgets already comes with pre-built extensions. Here are some of the available modules and the functionalities they add:
- Features: Compile kerning and mark features, rename, and subset features.
- Font: Scale, subset.
- Unicode: Unicode properties (script, direction).
- Glyph: Boolean operations, copying data between glyphs.
- Kerning: Manage kerning using a glyph-centered API.
- Groups: Manipulate kerning groups with a glyph-centered API.
- Interpolation: Generate instances with glyph swap rules applied.
- Git: Revert glyph data selectively (e.g. contours, width, etc) to a git commit.
## Warning
This package is currently in an alpha stage of development. While it is stable enough for adding methods to font objects, the public API may change in future versions. Please report any issues you encounter in the repository's issue tracker.

