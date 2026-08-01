
def _charString_from_SkPath(
    path: pathops.Path, charString: T2CharString
) -> T2CharString:
    if charString.width == charString.private.defaultWidthX:
        width = None
    else:
        width = charString.width - charString.private.nominalWidthX
    t2Pen = T2CharStringPen(width=width, glyphSet=None)
    path.draw(t2Pen)
    return t2Pen.getCharString(charString.private, charString.globalSubrs)

