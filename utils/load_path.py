
def load_path(filename: str | bytes) -> ImageFont:
    """
    Load font file. Same as :py:func:`~PIL.ImageFont.load`, but searches for a
    bitmap font along the Python path.

    :param filename: Name of font file.
    :return: A font object.
    :exception OSError: If the file could not be read.
    """
    if not isinstance(filename, str):
        filename = filename.decode("utf-8")
    for directory in sys.path:
        try:
            return load(os.path.join(directory, filename))
        except OSError:  # noqa: PERF203
            pass
    msg = f'cannot find font file "{filename}" in sys.path'
    if os.path.exists(filename):
        msg += f', did you mean ImageFont.load("{filename}") instead?'

    raise OSError(msg)

