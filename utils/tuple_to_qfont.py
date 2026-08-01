
def tuple_to_qfont(tup):
    """
    Create a QFont from tuple:
        (family [string], size [int], italic [bool], bold [bool])
    """
    if not (isinstance(tup, tuple) and len(tup) == 4
            and font_is_installed(tup[0])
            and isinstance(tup[1], Integral)
            and isinstance(tup[2], bool)
            and isinstance(tup[3], bool)):
        return None
    font = QtGui.QFont()
    family, size, italic, bold = tup
    font.setFamily(family)
    font.setPointSize(size)
    font.setItalic(italic)
    font.setBold(bold)
    return font

