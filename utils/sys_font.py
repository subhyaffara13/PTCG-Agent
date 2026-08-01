
def SysFont(name, size, bold=False, italic=False, constructor=None):
    """pygame.ftfont.SysFont(name, size, bold=False, italic=False, constructor=None) -> Font
    Create a pygame Font from system font resources.

    This will search the system fonts for the given font
    name. You can also enable bold or italic styles, and
    the appropriate system font will be selected if available.

    This will always return a valid Font object, and will
    fallback on the builtin pygame font if the given font
    is not found.

    Name can also be an iterable of font names, a string of
    comma-separated font names, or a bytes of comma-separated
    font names, in which case the set of names will be searched
    in order. Pygame uses a small set of common font aliases. If the
    specific font you ask for is not available, a reasonable
    alternative may be used.

    If optional constructor is provided, it must be a function with
    signature constructor(fontpath, size, bold, italic) which returns
    a Font instance. If None, a pygame.freetype.Font object is created.
    """
    if constructor is None:

        def constructor(fontpath, size, bold, italic):
            font = Font(fontpath, size)
            font.strong = bold
            font.oblique = italic
            return font

    return _SysFont(name, size, bold, italic, constructor)


def SysFont(name, size, bold=0, italic=0, constructor=None):
    """pygame.ftfont.SysFont(name, size, bold=False, italic=False, constructor=None) -> Font
    Create a pygame Font from system font resources.

    This will search the system fonts for the given font
    name. You can also enable bold or italic styles, and
    the appropriate system font will be selected if available.

    This will always return a valid Font object, and will
    fallback on the builtin pygame font if the given font
    is not found.

    Name can also be an iterable of font names, a string of
    comma-separated font names, or a bytes of comma-separated
    font names, in which case the set of names will be searched
    in order. Pygame uses a small set of common font aliases. If the
    specific font you ask for is not available, a reasonable
    alternative may be used.

    If optional constructor is provided, it must be a function with
    signature constructor(fontpath, size, bold, italic) which returns
    a Font instance. If None, a pygame.ftfont.Font object is created.
    """
    if constructor is None:

        def constructor(fontpath, size, bold, italic):
            font = Font(fontpath, size)
            font.set_bold(bold)
            font.set_italic(italic)
            return font

    return _SysFont(name, size, bold, italic, constructor)


def SysFont(name, size, bold=False, italic=False, constructor=None):
    """pygame.font.SysFont(name, size, bold=False, italic=False, constructor=None) -> Font
    Create a pygame Font from system font resources.

    This will search the system fonts for the given font
    name. You can also enable bold or italic styles, and
    the appropriate system font will be selected if available.

    This will always return a valid Font object, and will
    fallback on the builtin pygame font if the given font
    is not found.

    Name can also be an iterable of font names, a string of
    comma-separated font names, or a bytes of comma-separated
    font names, in which case the set of names will be searched
    in order. Pygame uses a small set of common font aliases. If the
    specific font you ask for is not available, a reasonable
    alternative may be used.

    If optional constructor is provided, it must be a function with
    signature constructor(fontpath, size, bold, italic) which returns
    a Font instance. If None, a pygame.font.Font object is created.
    """
    if constructor is None:
        constructor = font_constructor

    initsysfonts()

    gotbold = gotitalic = False
    fontname = None
    if name:
        if isinstance(name, (str, bytes)):
            name = name.split(b"," if isinstance(name, bytes) else ",")
        for single_name in name:
            if isinstance(single_name, bytes):
                single_name = single_name.decode()

            single_name = _simplename(single_name)
            styles = Sysfonts.get(single_name)
            if not styles:
                styles = Sysalias.get(single_name)
            if styles:
                plainname = styles.get((False, False))
                fontname = styles.get((bold, italic))
                if not (fontname or plainname):
                    # Neither requested style, nor plain font exists, so
                    # return a font with the name requested, but an
                    # arbitrary style.
                    (style, fontname) = list(styles.items())[0]
                    # Attempt to style it as requested. This can't
                    # unbold or unitalicize anything, but it can
                    # fake bold and/or fake italicize.
                    if bold and style[0]:
                        gotbold = True
                    if italic and style[1]:
                        gotitalic = True
                elif not fontname:
                    fontname = plainname
                elif plainname != fontname:
                    gotbold = bold
                    gotitalic = italic
            if fontname:
                break

    set_bold = set_italic = False
    if bold and not gotbold:
        set_bold = True
    if italic and not gotitalic:
        set_italic = True

    return constructor(fontname, size, set_bold, set_italic)

