
def _glyphComponentToUnicode(component, isZapfDingbats):
    # If the font is Zapf Dingbats (PostScript FontName: ZapfDingbats),
    # and the component is in the ITC Zapf Dingbats Glyph List, then
    # map it to the corresponding character in that list.
    dingbat = _zapfDingbatsToUnicode(component) if isZapfDingbats else None
    if dingbat:
        return dingbat

    # Otherwise, if the component is in AGL, then map it
    # to the corresponding character in that list.
    uchars = LEGACY_AGL2UV.get(component)
    if uchars:
        return "".join(map(chr, uchars))

    # Otherwise, if the component is of the form "uni" (U+0075,
    # U+006E, and U+0069) followed by a sequence of uppercase
    # hexadecimal digits (0–9 and A–F, meaning U+0030 through
    # U+0039 and U+0041 through U+0046), if the length of that
    # sequence is a multiple of four, and if each group of four
    # digits represents a value in the ranges 0000 through D7FF
    # or E000 through FFFF, then interpret each as a Unicode scalar
    # value and map the component to the string made of those
    # scalar values. Note that the range and digit-length
    # restrictions mean that the "uni" glyph name prefix can be
    # used only with UVs in the Basic Multilingual Plane (BMP).
    uni = _uniToUnicode(component)
    if uni:
        return uni

    # Otherwise, if the component is of the form "u" (U+0075)
    # followed by a sequence of four to six uppercase hexadecimal
    # digits (0–9 and A–F, meaning U+0030 through U+0039 and
    # U+0041 through U+0046), and those digits represents a value
    # in the ranges 0000 through D7FF or E000 through 10FFFF, then
    # interpret it as a Unicode scalar value and map the component
    # to the string made of this scalar value.
    uni = _uToUnicode(component)
    if uni:
        return uni

    # Otherwise, map the component to an empty string.
    return ""

