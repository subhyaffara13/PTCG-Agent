
def _get_numpy_version() -> tuple[str, str, str]:
    """
    Return the numpy version number if numpy can be imported.

    Otherwise returns ('0', '0', '0')
    """
    try:
        import numpy  # pylint: disable=import-outside-toplevel

        return tuple(numpy.version.version.split("."))
    except (ImportError, AttributeError):
        return ("0", "0", "0")

