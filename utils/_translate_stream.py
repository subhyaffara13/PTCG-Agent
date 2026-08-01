
def _translate_stream(stream, translation):
    """
    >>> import io
    >>> _translate_stream(io.StringIO('foo'), to_dvorak)
    urr
    """
    print(translate(stream.read(), translation))

