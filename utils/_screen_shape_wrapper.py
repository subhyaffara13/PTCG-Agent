
def _screen_shape_wrapper():  # pragma: no cover
    """
    Return a function which returns console dimensions (width, height).
    Supported: linux, osx, windows, cygwin.
    """
    def inner(fp):
        try:
            from os import get_terminal_size
            cols, lines = get_terminal_size(getattr(fp, 'fileno', lambda: None)())
            return cols - 1, lines - 1
        except Exception:
            return None, None

    return inner

