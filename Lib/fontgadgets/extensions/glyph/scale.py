from fontgadgets.decorators import *
from fontTools.misc.roundTools import otRound
from typing import Tuple, Union

@font_method
def scale(
    glyph: defcon.Glyph,
    factor: Union[float, Tuple[float, float]],
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
        factor (float or tuple): The scaling factor. If a tuple is provided,
            it will be interpreted as (x, y) for non-uniform scaling.
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
    if isinstance(factor, (int, float)):
        factor_x = factor_y = factor
    else:
        factor_x, factor_y = factor

    def scale_and_round_x(value: float) -> float:
        v = value * factor_x
        return otRound(v) if round_values else v

    def scale_and_round_y(value: float) -> float:
        v = value * factor_y
        return otRound(v) if round_values else v

    if contours and len(glyph) > 0:
        for contour in glyph:
            for point in contour:
                point.x = scale_and_round_x(point.x)
                point.y = scale_and_round_y(point.y)

    if anchors:
        for anchor in glyph.anchors:
            anchor.x = scale_and_round_x(anchor.x)
            anchor.y = scale_and_round_y(anchor.y)

    if guidelines:
        for guideline in glyph.guidelines:
            if guideline.x is not None:
                guideline.x = scale_and_round_x(guideline.x)
            if guideline.y is not None:
                guideline.y = scale_and_round_y(guideline.y)

    if components:
        for c in glyph.components:
            xScale, xyScale, yxScale, yScale, xOffset, yOffset = c.transformation
            xOffset = scale_and_round_x(xOffset)
            yOffset = scale_and_round_y(yOffset)
            c.transformation = (xScale, xyScale, yxScale, yScale, xOffset, yOffset)

    if width:
        glyph.width = scale_and_round_x(glyph.width)