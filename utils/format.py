
def format(validator, format, instance, schema):
    if validator.format_checker is not None:
        try:
            validator.format_checker.check(instance, format)
        except FormatError as error:
            yield ValidationError(error.message, cause=error.cause)


def format(url: URL) -> str:  # noqa: A001
    result = ""

    result += url.protocol or ""
    result += "//" if url.slashes else ""
    result += url.auth + "@" if url.auth else ""

    if url.hostname and ":" in url.hostname:
        # ipv6 address
        result += "[" + url.hostname + "]"
    else:
        result += url.hostname or ""

    result += ":" + url.port if url.port else ""
    result += url.pathname or ""
    result += url.search or ""
    result += url.hash or ""

    return result


def format(tokens, formatter, outfile=None):  # pylint: disable=redefined-builtin
    """
    Format ``tokens`` (an iterable of tokens) with the formatter ``formatter``
    (a `Formatter` instance).

    If ``outfile`` is given and a valid file object (an object with a
    ``write`` method), the result will be written to it, otherwise it
    is returned as a string.
    """
    try:
        if not outfile:
            realoutfile = getattr(formatter, 'encoding', None) and BytesIO() or StringIO()
            formatter.format(tokens, realoutfile)
            return realoutfile.getvalue()
        else:
            formatter.format(tokens, outfile)
    except TypeError:
        # Heuristic to catch a common mistake.
        from pygments.formatter import Formatter
        if isinstance(formatter, type) and issubclass(formatter, Formatter):
            raise TypeError('format() argument must be a formatter instance, '
                            'not a class')
        raise


def format(tokens, formatter, outfile=None):  # pylint: disable=redefined-builtin
    """
    Format ``tokens`` (an iterable of tokens) with the formatter ``formatter``
    (a `Formatter` instance).

    If ``outfile`` is given and a valid file object (an object with a
    ``write`` method), the result will be written to it, otherwise it
    is returned as a string.
    """
    try:
        if not outfile:
            realoutfile = getattr(formatter, 'encoding', None) and BytesIO() or StringIO()
            formatter.format(tokens, realoutfile)
            return realoutfile.getvalue()
        else:
            formatter.format(tokens, outfile)
    except TypeError:
        # Heuristic to catch a common mistake.
        from pip._vendor.pygments.formatter import Formatter
        if isinstance(formatter, type) and issubclass(formatter, Formatter):
            raise TypeError('format() argument must be a formatter instance, '
                            'not a class')
        raise

