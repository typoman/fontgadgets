from fontgadgets.decorators import *
from fontTools.misc.roundTools import otRound

@font_method
def scale(
    glyph: defcon.Glyph,
    factor: float,
    *,
    round_values: bool = True,
    contours: bool = True,
    anchors: bool = True,
    guidelines: bool = True,
    components: bool = True,
    width: bool = True,
):
    """
    Scale the contours, anchors, guidelines, components and width
    of the glyph by factor.

    Args:
        factor (float): The scaling factor.
        round_values (bool, optional): Whether to round the scaled values.
            Defaults to True.
        contours (bool, optional): Whether to scale the contours.
            Defaults to True.
        anchors (bool, optional): Whether to scale the anchors.
            Defaults to True.
        guidelines (bool, optional): Whether to scale the guidelines.
            Defaults to True.
        components (bool, optional): Whether to scale the components.
            Defaults to True.
        width (bool, optional): Whether to scale the glyph width.
            Defaults to True.
    """
    def scale_and_round(value: float) -> float:
        v = value * factor
        return otRound(v) if round_values else v

    if contours and len(glyph) > 0:
        for contour in glyph:
            for point in contour:
                point.x = scale_and_round(point.x)
                point.y = scale_and_round(point.y)

    if anchors:
        for anchor in glyph.anchors:
            anchor.x = scale_and_round(anchor.x)
            anchor.y = scale_and_round(anchor.y)

    if guidelines:
        for guideline in glyph.guidelines:
            if guideline.x is not None:
                guideline.x = scale_and_round(guideline.x)
            if guideline.y is not None:
                guideline.y = scale_and_round(guideline.y)

    if components:
        for c in glyph.components:
            xScale, xyScale, yxScale, yScale, xOffset, yOffset = c.transformation
            xOffset = scale_and_round(xOffset)
            yOffset = scale_and_round(yOffset)
            c.transformation = (xScale, xyScale, yxScale, yScale, xOffset, yOffset)

    if width:
        glyph.width = scale_and_round(glyph.width)
