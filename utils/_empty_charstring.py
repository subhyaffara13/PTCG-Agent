
def _empty_charstring(font, glyphName, isCFF2, ignoreWidth=False):
    c, fdSelectIndex = font.CharStrings.getItemAndSelector(glyphName)
    if isCFF2 or ignoreWidth:
        # CFF2 charstrings have no widths nor 'endchar' operators
        c.setProgram([] if isCFF2 else ["endchar"])
    else:
        if hasattr(font, "FDArray") and font.FDArray is not None:
            private = font.FDArray[fdSelectIndex].Private
        else:
            private = font.Private
        dfltWdX = private.defaultWidthX
        nmnlWdX = private.nominalWidthX
        pen = NullPen()
        c.draw(pen)  # this will set the charstring's width
        if c.width != dfltWdX:
            c.program = [c.width - nmnlWdX, "endchar"]
        else:
            c.program = ["endchar"]

