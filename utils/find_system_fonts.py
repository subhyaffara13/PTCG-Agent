
def findSystemFonts(fontpaths=None, fontext='ttf'):
    """
    Find fonts in a search path, system paths, or some other platform-specific method.

    Parameters
    ----------
    fontpaths : list of str, optional
        Search for fonts in these specified font paths. If no paths are given and the
        :envvar:`MPL_IGNORE_SYSTEM_FONTS` is not set, use a standard set of system
        paths, as well as the list of fonts tracked by fontconfig if fontconfig is
        installed and available.
    fontext : {'ttf', 'afm'}, default: 'ttf'
        If 'ttf', search for TrueType fonts; if 'afm', search for with AFM fonts.

    Returns
    -------
    list of str
        A list of file paths with fonts of the given type.
    """
    fontfiles = set()
    fontexts = get_fontext_synonyms(fontext)

    if fontpaths is None:
        if os.getenv('MPL_IGNORE_SYSTEM_FONTS'):
            installed_fonts = []
            fontpaths = []
        elif sys.platform == 'win32':
            installed_fonts = _get_win32_installed_fonts()
            fontpaths = []
        elif sys.platform == 'emscripten':
            installed_fonts = []
            fontpaths = []
        else:
            installed_fonts = _get_fontconfig_fonts()
            if sys.platform == 'darwin':
                installed_fonts += _get_macos_fonts()
                fontpaths = [*X11FontDirectories, *OSXFontDirectories]
            else:
                fontpaths = X11FontDirectories
        fontfiles.update(str(path) for path in installed_fonts
                         if path.suffix.lower()[1:] in fontexts)

    elif isinstance(fontpaths, str):
        fontpaths = [fontpaths]

    for path in fontpaths:
        fontfiles.update(map(os.path.abspath, list_fonts(path, fontexts)))

    return [fname for fname in fontfiles if os.path.exists(fname)]

