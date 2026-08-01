
def get_fonts():
    """pygame.font.get_fonts() -> list
    get a list of system font names

    Returns the list of all found system fonts. Note that
    the names of the fonts will be all lowercase with spaces
    removed. This is how pygame internally stores the font
    names for matching.
    """
    initsysfonts()
    return list(Sysfonts)

