
def check_palette(palette):
    """Check a palette argument (to the :class:`Writer` class) for validity.
    Returns the palette as a list if okay; raises an exception otherwise.
    """

    # None is the default and is allowed.
    if palette is None:
        return None

    p = list(palette)
    if not (0 < len(p) <= 256):
        raise ValueError("a palette must have between 1 and 256 entries")
    seen_triple = False
    for i, t in enumerate(p):
        if len(t) not in (3, 4):
            raise ValueError("palette entry %d: entries must be 3- or 4-tuples." % i)
        if len(t) == 3:
            seen_triple = True
        if seen_triple and len(t) == 4:
            raise ValueError(
                "palette entry %d: all 4-tuples must precede all 3-tuples" % i
            )
        for x in t:
            if int(x) != x or not (0 <= x <= 255):
                raise ValueError(
                    "palette entry %d: values must be integer: 0 <= x <= 255" % i
                )
    return p

