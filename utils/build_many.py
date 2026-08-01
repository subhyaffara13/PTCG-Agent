
def build_many(
    designspace: DesignSpaceDocument,
    master_finder=lambda s: s,
    exclude=[],
    optimize=True,
    skip_vf=lambda vf_name: False,
    colr_layer_reuse=True,
    drop_implied_oncurves=False,
):
    """
    Build variable fonts from a designspace file, version 5 which can define
    several VFs, or version 4 which has implicitly one VF covering the whole doc.

    If master_finder is set, it should be a callable that takes master
    filename as found in designspace file and map it to master font
    binary as to be opened (eg. .ttf or .otf).

    skip_vf can be used to skip building some of the variable fonts defined in
    the input designspace. It's a predicate that takes as argument the name
    of the variable font and returns `bool`.

    Always returns a Dict[str, TTFont] keyed by VariableFontDescriptor.name
    """
    res = {}
    # varLib.build (used further below) by default only builds an incomplete 'STAT'
    # with an empty AxisValueArray--unless the VF inherited 'STAT' from its base master.
    # Designspace version 5 can also be used to define 'STAT' labels or customize
    # axes ordering, etc. To avoid overwriting a pre-existing 'STAT' or redoing the
    # same work twice, here we check if designspace contains any 'STAT' info before
    # proceeding to call buildVFStatTable for each VF.
    # https://github.com/fonttools/fonttools/pull/3024
    # https://github.com/fonttools/fonttools/issues/3045
    doBuildStatFromDSv5 = (
        "STAT" not in exclude
        and designspace.formatTuple >= (5, 0)
        and (
            any(a.axisLabels or a.axisOrdering is not None for a in designspace.axes)
            or designspace.locationLabels
        )
    )
    for _location, subDoc in splitInterpolable(designspace):
        for name, vfDoc in splitVariableFonts(subDoc):
            if skip_vf(name):
                log.debug(f"Skipping variable TTF font: {name}")
                continue
            vf = build(
                vfDoc,
                master_finder,
                exclude=exclude,
                optimize=optimize,
                colr_layer_reuse=colr_layer_reuse,
                drop_implied_oncurves=drop_implied_oncurves,
            )[0]
            if doBuildStatFromDSv5:
                buildVFStatTable(vf, designspace, name)
            res[name] = vf
    return res

