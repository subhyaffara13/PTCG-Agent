
def merge_charstrings(glyphOrder, num_masters, top_dicts, masterModel):
    vsindex_dict = {}
    vsindex_by_key = {}
    varDataList = []
    masterSupports = []
    default_charstrings = top_dicts[0].CharStrings
    for gid, gname in enumerate(glyphOrder):
        # interpret empty non-default masters as missing glyphs from a sparse master
        all_cs = [
            _get_cs(td.CharStrings, gname, i != 0) for i, td in enumerate(top_dicts)
        ]
        model, model_cs = masterModel.getSubModel(all_cs)
        # create the first pass CFF2 charstring, from
        # the default charstring.
        default_charstring = model_cs[0]
        var_pen = CFF2CharStringMergePen([], gname, num_masters, 0)
        # We need to override outlineExtractor because these
        # charstrings do have widths in the 'program'; we need to drop these
        # values rather than post assertion error for them.
        default_charstring.outlineExtractor = MergeOutlineExtractor
        default_charstring.draw(var_pen)

        # Add the coordinates from all the other regions to the
        # blend lists in the CFF2 charstring.
        region_cs = model_cs[1:]
        for region_idx, region_charstring in enumerate(region_cs, start=1):
            var_pen.restart(region_idx)
            region_charstring.outlineExtractor = MergeOutlineExtractor
            region_charstring.draw(var_pen)

        # Collapse each coordinate list to a blend operator and its args.
        new_cs = var_pen.getCharString(
            private=default_charstring.private,
            globalSubrs=default_charstring.globalSubrs,
            var_model=model,
            optimize=True,
        )
        default_charstrings[gname] = new_cs

        if not region_cs:
            continue

        if (not var_pen.seen_moveto) or ("blend" not in new_cs.program):
            # If this is not a marking glyph, or if there are no blend
            # arguments, then we can use vsindex 0. No need to
            # check if we need a new vsindex.
            continue

        # If the charstring required a new model, create
        # a VarData table to go with, and set vsindex.
        key = tuple(v is not None for v in all_cs)
        try:
            vsindex = vsindex_by_key[key]
        except KeyError:
            vsindex = _add_new_vsindex(
                model, key, masterSupports, vsindex_dict, vsindex_by_key, varDataList
            )
        # We do not need to check for an existing new_cs.private.vsindex,
        # as we know it doesn't exist yet.
        if vsindex != 0:
            new_cs.program[:0] = [vsindex, "vsindex"]

    # If there is no variation in any of the charstrings, then vsindex_dict
    # never gets built. This could still be needed if there is variation
    # in the PrivatDict, so we will build the default data for vsindex = 0.
    if not vsindex_dict:
        key = (True,) * num_masters
        _add_new_vsindex(
            masterModel, key, masterSupports, vsindex_dict, vsindex_by_key, varDataList
        )
    cvData = CVarData(
        varDataList=varDataList,
        masterSupports=masterSupports,
        vsindex_dict=vsindex_dict,
    )
    # XXX To do: optimize use of vsindex between the PrivateDicts and
    # charstrings
    return cvData

