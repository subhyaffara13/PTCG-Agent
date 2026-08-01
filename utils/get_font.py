
def get_font(font_filepaths, hinting_factor=None):
    """
    Get an `.ft2font.FT2Font` object given a list of file paths.

    Parameters
    ----------
    font_filepaths : Iterable[str, bytes, os.PathLike, FontPath], \
str, bytes, os.PathLike, FontPath
        Relative or absolute paths to the font files to be used.

        If a single string, bytes, or `os.PathLike`, then it will be treated
        as a list with that entry only.

        If more than one filepath is passed, then the returned FT2Font object
        will fall back through the fonts, in the order given, to find a needed
        glyph.

    Returns
    -------
    `.ft2font.FT2Font`

    """
    match font_filepaths:
        case FontPath(path, index):
            paths = ((_cached_realpath(path), index), )
        case str() | bytes() | os.PathLike() as path:
            paths = ((_cached_realpath(path), 0), )
        case _:
            paths = tuple(
                (_cached_realpath(fname.path), fname.face_index)
                if isinstance(fname, FontPath) else (_cached_realpath(fname), 0)
                for fname in font_filepaths)

    font = _get_font(
        # must be a tuple to be cached
        paths,
        _kerning_factor=mpl.rcParams['text.kerning_factor'],
        # also key on the thread ID to prevent segfaults with multi-threading
        thread_id=threading.get_ident(),
        enable_last_resort=mpl.rcParams['font.enable_last_resort'],
    )
    # Ensure the transform is always consistent.
    font._set_transform([[0x10000, 0], [0, 0x10000]], [0, 0])
    return font


def get_font(path, size):
    from os import path as os_path

    cwd = os_path.dirname(__file__)
    font = pygame.font.Font((cwd + "/" + path), size)
    return font


def get_font(path, size):
    from os import path as os_path

    cwd = os_path.dirname(__file__)
    font = pygame.font.Font((cwd + "/" + path), size)
    return font


def get_font(path, size):
    from os import path as os_path

    cwd = os_path.dirname(__file__)
    font = pygame.font.Font((cwd + "/" + path), size)
    return font


def get_font(path, size):
    from os import path as os_path

    cwd = os_path.dirname(__file__)
    font = pygame.font.Font((cwd + "/" + path), size)
    return font


def get_font(path, size):
    from os import path as os_path

    cwd = os_path.dirname(__file__)
    font = pygame.font.Font((cwd + "/" + path), size)
    return font


def get_font(path, size):
    from os import path as os_path

    cwd = os_path.dirname(__file__)
    font = pygame.font.Font((cwd + "/" + path), size)
    return font

