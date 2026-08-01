
def _generate_sfnts(fontdata, font, breakpoints):
    """
    Transform font data into PostScript sfnts format.

    Helper function for _font_to_ps_type42.

    Parameters
    ----------
    fontdata : bytes
        The raw data of the font
    font : fontTools.ttLib.ttFont.TTFont
        The fontTools font object
    breakpoints : list
        Sorted offsets of possible breakpoints

    Returns
    -------
    str
        The sfnts array for the font definition, consisting
        of hex-encoded strings in PostScript format
    """
    s = '/sfnts['
    pos = 0
    while pos < len(fontdata):
        i = bisect.bisect_left(breakpoints, pos + 65534)
        newpos = breakpoints[i-1]
        if newpos <= pos:
            # have to accept a larger string
            newpos = breakpoints[-1]
        s += f'<{fontdata[pos:newpos].hex()}00>'  # Always NUL terminate.
        pos = newpos
    s += ']def'
    return '\n'.join(s[i:i+100] for i in range(0, len(s), 100))

