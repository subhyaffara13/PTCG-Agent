
def initsysfonts_darwin():
    """Read the fonts on MacOS, and OS X."""
    #  fc-list is not likely to be there on pre 10.4.x, or MacOS 10.10+
    fonts = {}

    fclist_locations = [
        "/usr/X11/bin/fc-list",  # apple x11
        "/usr/X11R6/bin/fc-list",  # apple x11
    ]
    for bin_location in fclist_locations:
        if exists(bin_location):
            fonts = initsysfonts_unix(bin_location)
            break

    if len(fonts) == 0:
        fonts = _font_finder_darwin()

    return fonts

