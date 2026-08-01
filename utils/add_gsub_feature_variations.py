
def addGSUBFeatureVariations(vf, designspace, featureTags=(), *, log_enabled=False):
    """Add GSUB FeatureVariations table to variable font, based on DesignSpace rules.

    Args:
        vf: A TTFont object representing the variable font.
        designspace: A DesignSpaceDocument object.
        featureTags: Optional feature tag(s) to use for the FeatureVariations records.
            If unset, the key 'com.github.fonttools.varLib.featureVarsFeatureTag' is
            looked up in the DS <lib> and used; otherwise the default is 'rclt' if
            the <rules processing="last"> attribute is set, else 'rvrn'.
            See <https://fonttools.readthedocs.io/en/latest/designspaceLib/xml.html#rules-element>
        log_enabled: If True, log info about DS axes and sources. Default is False, as
            the same info may have already been logged as part of varLib.build.
    """
    ds = load_designspace(designspace, log_enabled=log_enabled)
    if not ds.rules:
        return
    if not featureTags:
        featureTags = _feature_variations_tags(ds)
    _add_GSUB_feature_variations(
        vf, ds.axes, ds.internal_axis_supports, ds.rules, featureTags
    )

