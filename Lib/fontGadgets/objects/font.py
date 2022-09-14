from fontGadgets.tools import fontMethod
from fontParts.fontshell import RFont
import os
import shutil

def _scaleGlyph(glyph, factor):
    with glyph.undo():
        if glyph.contours:
            for contour in glyph:
                contour.scaleBy(factor)
        for anchor in glyph.anchors:
            anchor.scaleBy(factor)
        for guideline in glyph.guidelines:
            guideline.scaleBy(factor)
        for c in glyph.components:
            xScale, xyScale, yxScale, yScale, xOffset, yOffset = c.transformation
            xOffset *= factor
            yOffset *= factor
            c.transformation = xScale, xyScale, yxScale, yScale, xOffset, yOffset
        glyph.width *= factor

def _scaleRound(v, factor):
    return int(round(v * factor))

_scaleAttribues = [
    "descender",
    "xHeight",
    "capHeight",
    "ascender",
    # "unitsPerEm",
]

@fontMethod
def scale(font, factor=1, layerNames=None, roundValues=True):
    """
    Smalller values than 1 makes the font smaller.
    layerNames: list of name of layers you want to scale, if not provided then
    the default layer will be scaled.
    """
    layersToScale = []
    if layerNames is not None:
        layersToScale = [font.getLayer(l) for l in layerNames]
    if layersToScale == []:
        layersToScale = [font, ]
    for layer in layersToScale:
        for g in layersToScale:
            _scaleGlyph(g, factor)
    if font.kerning:
        font.kerning.scaleBy(factor)
        font.kerning.round(1)
    for a in _scaleAttribues:
        v = getattr(font.info, a)
        setattr(font.info, a, _scaleRound(v, factor))
    if roundValues:
        font.round()
    font.changed()

@fontMethod
def subset(font, glyphsToKeep, path=None):
    """
    Subsets and returns a copy of the font. If path is not provided, then
    the subset ufo file will be saved on the disk next to the font.path.
    """

    if path is None:
        path = os.path.normpath(font.path)
        ufoStem, ufoExtension = os.path.splitext(path)
        subsetUfoPath = '{}_subset{}'.format(ufoStem, ufoExtension)
    shutil.copytree(path, subsetUfoPath)
    subsetFont = RFont(subsetUfoPath)
    glyphsToKeep = set(glyphsToKeep)
    glyphsToRemove = set(subsetFont.keys()) - glyphsToKeep
    componentReferences = subsetFont.componentReferences

    for glyphToRemove in glyphsToRemove:
        if glyphToRemove in componentReferences:
            decomposeList = componentReferences[glyphToRemove]
            for glyphName in decomposeList:
                if glyphName in subsetFont.keys():
                    glyphToDecompose = subsetFont[glyphName]
                    [c.decompose() for c in glyphToDecompose.components if c.baseGlyph == glyphToRemove]
        if glyphToRemove in subsetFont:
            del subsetFont[glyphToRemove]

    newGlyphOrder = [gn for gn in subsetFont.lib['public.glyphOrder'] if gn in glyphsToKeep]
    subsetFont.lib['public.glyphOrder'] = newGlyphOrder
    if 'com.typemytype.robofont.sort' in subsetFont.lib.keys():
        del(subsetFont.lib['com.typemytype.robofont.sort'])

    newGroups = {}
    for groupName, glyphList in subsetFont.groups.items():
        glyphList = [g for g in glyphList if g in glyphsToKeep]
        if glyphList:
            newGroups[groupName] = glyphList
        subsetFont.groups.clear()
        subsetFont.groups.update(newGroups)

    newKerning = {}
    for pair, value in subsetFont.kerning.items():
        if subsetFont.kerning.isKerningPairValid(pair):
            newKerning[pair] = value

    subsetFont.features.text = str(font.features.subset(glyphsToKeep))
    subsetFont.kerning.clear()
    subsetFont.kerning.update(newKerning)
    subsetFont.save()
    return subsetFont

def testInstall(font):
    pass
