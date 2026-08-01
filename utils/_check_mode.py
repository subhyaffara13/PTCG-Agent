
def _check_mode(mode):
    mode = mode.lower()
    enum = mode_enum(mode)
    return enum


def _check_mode(mode, encoding, newline):
    """Check mode and that encoding and newline are compatible.

    Parameters
    ----------
    mode : str
        File open mode.
    encoding : str
        File encoding.
    newline : str
        Newline for text files.

    """
    if "t" in mode:
        if "b" in mode:
            raise ValueError(f"Invalid mode: {mode!r}")
    else:
        if encoding is not None:
            raise ValueError("Argument 'encoding' not supported in binary mode")
        if newline is not None:
            raise ValueError("Argument 'newline' not supported in binary mode")

