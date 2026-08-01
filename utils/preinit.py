
def preinit() -> None:
    """
    Explicitly loads BMP, GIF, JPEG, PPM and PNG file format drivers.

    It is called when opening or saving images.
    """

    global _initialized
    if _initialized >= 1:
        return

    try:
        from . import BmpImagePlugin

        assert BmpImagePlugin
    except ImportError:
        pass
    try:
        from . import GifImagePlugin

        assert GifImagePlugin
    except ImportError:
        pass
    try:
        from . import JpegImagePlugin

        assert JpegImagePlugin
    except ImportError:
        pass
    try:
        from . import PpmImagePlugin

        assert PpmImagePlugin
    except ImportError:
        pass
    try:
        from . import PngImagePlugin

        assert PngImagePlugin
    except ImportError:
        pass

    _initialized = 1

