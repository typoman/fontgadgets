import os
from fontTools.ufoLib.filenames import userNameToFileName
from mojo.roboFont import RGlyph
from fontTools.pens.cocoaPen import CocoaPen
from drawBot import BezierPath
from mojo.pens import DecomposePointPen

def getGlifPath(glyph, git=True):
    """
    returns path to the file which contains the glyph information.
    if git is True the glif path will be rturned relative to root
    of the git repo.
    """

    dglyph = glyph.naked()
    glifName = userNameToFileName(glyph.name, existing=[], suffix=".glif")
    folder = 'glyphs'
    if glyph.layer.name != 'public.default':
        folder += f".{glyph.layer.name}"
    path = os.path.join(glyph.font.path, folder, glifName)
    if git:
        dglyph._path = os.path.relpath(path, glyph.font.repo.working_dir)
    return dglyph._path

RGlyph.path = property(lambda self: getGlifPath(self))

def getStroked(glyph, strokeWidth):
    """
    Returns a stroked copy of the glyph
    """
    pen = CocoaPen(glyph.font)
    glyph.draw(pen)
    bezierPath = BezierPath(pen.path)
    bezierPath.removeOverlap()
    newPath = bezierPath.expandStroke(strokeWidth).removeOverlap()
    union = newPath.union(bezierPath)
    result = RGlyph()
    p = result.getPen()
    union.drawToPen(p)
    return result

RGlyph.getStroked = getStroked

def getDecomposed(glyph):
    """
    Returns a decomposed copy of the glyph
    """
    f = glyph.font
    decomposedGlyph = RGlyph()
    decomposedGlyph.name = glyph.name
    decomposedGlyph.width = glyph.width
    dstPen = decomposedGlyph.getPointPen()
    decomposePen = DecomposePointPen(f, dstPen)
    glyph.drawPoints(decomposePen)
    return decomposedGlyph

RGlyph.getDecomposed = getDecomposed
