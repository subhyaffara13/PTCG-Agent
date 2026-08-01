
def interpolate_cff2_metrics(varfont, topDict, glyphOrder, loc):
    """Unlike TrueType glyphs, neither advance width nor bounding box
    info is stored in a CFF2 charstring. The width data exists only in
    the hmtx and HVAR tables. Since LSB data cannot be interpolated
    reliably from the master LSB values in the hmtx table, we traverse
    the charstring to determine the actual bound box."""

    charstrings = topDict.CharStrings
    boundsPen = BoundsPen(glyphOrder)
    hmtx = varfont["hmtx"]
    hvar_table = None
    if "HVAR" in varfont:
        hvar_table = varfont["HVAR"].table
        fvar = varfont["fvar"]
        varStoreInstancer = VarStoreInstancer(hvar_table.VarStore, fvar.axes, loc)

    for gid, gname in enumerate(glyphOrder):
        entry = list(hmtx[gname])
        # get width delta.
        if hvar_table:
            if hvar_table.AdvWidthMap:
                width_idx = hvar_table.AdvWidthMap.mapping[gname]
            else:
                width_idx = gid
            width_delta = otRound(varStoreInstancer[width_idx])
        else:
            width_delta = 0

        # get LSB.
        boundsPen.init()
        charstring = charstrings[gname]
        charstring.draw(boundsPen)
        if boundsPen.bounds is None:
            # Happens with non-marking glyphs
            lsb_delta = 0
        else:
            lsb = otRound(boundsPen.bounds[0])
            lsb_delta = entry[1] - lsb

        if lsb_delta or width_delta:
            if width_delta:
                entry[0] = max(0, entry[0] + width_delta)
            if lsb_delta:
                entry[1] = lsb
            hmtx[gname] = tuple(entry)

