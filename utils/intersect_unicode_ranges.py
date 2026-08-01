
def intersectUnicodeRanges(unicodes, inverse=False):
    """Intersect a sequence of (int) Unicode codepoints with the Unicode block
    ranges defined in the OpenType specification v1.7, and return the set of
    'ulUnicodeRanges' bits for which there is at least ONE intersection.
    If 'inverse' is True, return the the bits for which there is NO intersection.

    >>> intersectUnicodeRanges([0x0410]) == {9}
    True
    >>> intersectUnicodeRanges([0x0410, 0x1F000]) == {9, 57, 122}
    True
    >>> intersectUnicodeRanges([0x0410, 0x1F000], inverse=True) == (
    ...     set(range(len(OS2_UNICODE_RANGES))) - {9, 57, 122})
    True
    """
    unicodes = set(unicodes)
    unicodestarts, unicodevalues = _getUnicodeRanges()
    bits = set()
    for code in unicodes:
        stop, bit = unicodevalues[bisect.bisect(unicodestarts, code)]
        if code <= stop:
            bits.add(bit)
    # The spec says that bit 57 ("Non Plane 0") implies that there's
    # at least one codepoint beyond the BMP; so I also include all
    # the non-BMP codepoints here
    if any(0x10000 <= code < 0x110000 for code in unicodes):
        bits.add(57)
    return set(range(len(OS2_UNICODE_RANGES))) - bits if inverse else bits

