from .shaper import HBShaper
from .paragraph import *
# based on drawbot-skia

def alignGlyphPositionsInLine(glyphRecords, align):
    """
    Aligns the glyph positions based on the given alignment.

    Args:
        glyphRecords (SimpleNamespace): The glyph information.
        align (str, optional): The alignment. Defaults to None.
    """
    textWidth = glyphRecords[-1].position[0]
    if align is None:
        align = "left"
    xOffset = 0
    if align == "right":
        xOffset = -textWidth
    elif align == "center":
        xOffset = -textWidth / 2
    glyphRecords.positions = [(x + xOffset, y) for x, y in glyphRecords.positions]


class Layout:
    """
    A text layout engine that calculates glyph positions for a given text string.

    This class uses HarfBuzz for shaping and paragraph layout to determine the
    positions of each glyph in the text. It supports features like text direction,
    OpenType features, language/script settings, font variations, and text alignment.

    Args:
        font: The font object to use for text layout and glyph information.

    Example:
        >>> layout = Layout(font)
        >>> positions = layout.getGlyphNamesAndPositionsFromText(
        ...     "Hello World", 
        ...     direction="ltr",
        ...     align="center"
        ... )
        >>> for glyph_name, (x, y) in positions:
        ...     print(f"{glyph_name}: ({x}, {y})")
    """

    def __init__(self, font):
        """
        Initializes the Layout with the given font.

        Args:
            font (defcon.Font)
        """
        self._font = font

    def getGlyphNamesAndPositionsFromText(
        self,
        txt,
        features=None,
        direction=None,
        language=None,
        script=None,
        variations=None,
        offset=None,
        align=None,
        lineWidth=None,
        lineGap=None,
    ):
        """
        Gets the glyph names and final positions from the given text.

        Args:
            txt (str): The text to get glyph names and positions from.
            direction (int, optional): The text direction. Defaults to None.
            features (dict, optional): The font features. {feat_tag: False/True, ...}
            language (str, optional): The language.
            script (str, optional): The script.
            variations (dict, optional): The font variations. {axis_tag: value, ...}
            offset (tuple, optional): The offset. Defaults to None.
            align (str, optional): The alignment. Defaults to None.
            lineWidth (float, optional): The maximum line width. If None, no
            line breaking occurs.
            lineGap (float, optional): The line spacing, if None, it will be 
            taken from font ascender and descenders.

        Returns:
            list: A list of tuples containing the glyph name and position.
        """
        if not txt:
            return []

        if lineWidth is None:
            lineWidth = float("inf")

        paragraph = Paragraph(baseLevel=direction, width=lineWidth)
        paragraph.addTextFromFont(txt, self._font, 
                                    features=features,
                                    language=language,
                                    script=script,
                                    variations=variations
                                  )
        paragraph.calculateGlyphLines()

        x, y = (0, 0) if offset is None else offset
        fontEm = self._font.info.ascender - self._font.info.descender
        lineGap = 0 if lineGap is None else lineGap
        lineGap += fontEm
        result = []
        for i, line in enumerate(paragraph.glyphLines):
            gline = []
            currentX, currentY = x, y
            for record in line.glyphRecords:
                ax, ay = record.advance
                ox, oy = record.offset
                gx, gy = currentX + ox, currentY + oy
                gline.append((record.glyph.name, (gx, gy + (-lineGap * i))))
                currentX += ax
                currentY += ay
            if align:
                gline = alignGlyphPositionsInLine(gline, align)
            result.extend(gline)
        return result


