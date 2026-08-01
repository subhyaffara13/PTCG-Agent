
def ToASCII(label: str) -> bytes:
    """Compatibility shim for :rfc:`3490` ``ToASCII``.

    Delegates to :func:`idna.encode` (IDNA 2008). Provided to ease porting
    of code written against the legacy :mod:`encodings.idna` API; new code
    should call :func:`idna.encode` directly.

    :param label: The label or domain to encode.
    :returns: The encoded form as ASCII :class:`bytes`.
    """
    return encode(label)


def to_ascii(obj: str) -> str:
    def mapping(obj: str) -> str:
        if REGEX_NON_ASCII.search(obj):
            return "xn--" + encode(obj)
        return obj

    return map_domain(obj, mapping)


def ToASCII(label: str) -> bytes:
    return encode(label)

