
def color_triple(color):
    """
    Convert a command line colour value to a RGB triple of integers.
    FIXME: Somewhere we need support for greyscale backgrounds etc.
    """
    if color.startswith("#") and len(color) == 4:
        return (int(color[1], 16), int(color[2], 16), int(color[3], 16))
    if color.startswith("#") and len(color) == 7:
        return (int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16))
    elif color.startswith("#") and len(color) == 13:
        return (int(color[1:5], 16), int(color[5:9], 16), int(color[9:13], 16))

