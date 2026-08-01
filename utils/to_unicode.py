
def toUnicode(glyph, isZapfDingbats=False):
    """Convert glyph names to Unicode, such as ``'longs_t.oldstyle'`` --> ``u'ſt'``

    If ``isZapfDingbats`` is ``True``, the implementation recognizes additional
    glyph names (as required by the AGL specification).
    """
    # https://github.com/adobe-type-tools/agl-specification#2-the-mapping
    #
    # 1. Drop all the characters from the glyph name starting with
    #    the first occurrence of a period (U+002E; FULL STOP), if any.
    glyph = glyph.split(".", 1)[0]

    # 2. Split the remaining string into a sequence of components,
    #    using underscore (U+005F; LOW LINE) as the delimiter.
    components = glyph.split("_")

    # 3. Map each component to a character string according to the
    #    procedure below, and concatenate those strings; the result
    #     is the character string to which the glyph name is mapped.
    result = [_glyphComponentToUnicode(c, isZapfDingbats) for c in components]
    return "".join(result)


def ToUnicode(label: Union[bytes, bytearray]) -> str:
    """Compatibility shim for :rfc:`3490` ``ToUnicode``.

    Delegates to :func:`idna.decode` (IDNA 2008). Provided to ease porting
    of code written against the legacy :mod:`encodings.idna` API; new code
    should call :func:`idna.decode` directly.

    :param label: The label or domain to decode.
    :returns: The decoded Unicode form.
    """
    return decode(label)


def to_unicode(obj: str) -> str:
    def mapping(obj: str) -> str:
        if obj.startswith("xn--"):
            return decode(obj[4:].lower())
        return obj

    return map_domain(obj, mapping)


def ToUnicode(label: Union[bytes, bytearray]) -> str:
    return decode(label)

