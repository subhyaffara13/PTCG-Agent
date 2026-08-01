
def interpolate_layout(designspace, loc, master_finder=lambda s: s, mapped=False):
    """
    Interpolate GPOS from a designspace file and location.

    If master_finder is set, it should be a callable that takes master
    filename as found in designspace file and map it to master font
    binary as to be opened (eg. .ttf or .otf).

    If mapped is False (default), then location is mapped using the
    map element of the axes in designspace file.  If mapped is True,
    it is assumed that location is in designspace's internal space and
    no mapping is performed.
    """
    if hasattr(designspace, "sources"):  # Assume a DesignspaceDocument
        pass
    else:  # Assume a file path
        from fontTools.designspaceLib import DesignSpaceDocument

        designspace = DesignSpaceDocument.fromfile(designspace)

    ds = load_designspace(designspace)
    log.info("Building interpolated font")

    log.info("Loading master fonts")
    master_fonts = load_masters(designspace, master_finder)
    font = deepcopy(master_fonts[ds.base_idx])

    log.info("Location: %s", pformat(loc))
    if not mapped:
        loc = {name: ds.axes[name].map_forward(v) for name, v in loc.items()}
    log.info("Internal location: %s", pformat(loc))
    loc = models.normalizeLocation(loc, ds.internal_axis_supports)
    log.info("Normalized location: %s", pformat(loc))

    # Assume single-model for now.
    model = models.VariationModel(ds.normalized_master_locs)
    assert 0 == model.mapping[ds.base_idx]

    merger = InstancerMerger(font, model, loc)

    log.info("Building interpolated tables")
    # TODO GSUB/GDEF
    merger.mergeTables(font, master_fonts, ["GPOS"])
    return font

