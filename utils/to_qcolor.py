
def to_qcolor(color):
    """Create a QColor from a matplotlib color"""
    qcolor = QtGui.QColor()
    try:
        rgba = mcolors.to_rgba(color)
    except ValueError:
        _api.warn_external(f'Ignoring invalid color {color!r}')
        return qcolor  # return invalid QColor
    qcolor.setRgbF(*rgba)
    return qcolor

