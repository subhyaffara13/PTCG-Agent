
def addFeatureVariations(font, conditionalSubstitutions, featureTag="rvrn"):
    """Add conditional substitutions to a Variable Font.

    The `conditionalSubstitutions` argument is a list of (Region, Substitutions)
    tuples.

    A Region is a list of Boxes. A Box is a dict mapping axisTags to
    (minValue, maxValue) tuples. Irrelevant axes may be omitted and they are
    interpretted as extending to end of axis in each direction.  A Box represents
    an orthogonal 'rectangular' subset of an N-dimensional design space.
    A Region represents a more complex subset of an N-dimensional design space,
    ie. the union of all the Boxes in the Region.
    For efficiency, Boxes within a Region should ideally not overlap, but
    functionality is not compromised if they do.

    The minimum and maximum values are expressed in normalized coordinates.

    A Substitution is a dict mapping source glyph names to substitute glyph names.

    Example:

    # >>> f = TTFont(srcPath)
    # >>> condSubst = [
    # ...     # A list of (Region, Substitution) tuples.
    # ...     ([{"wdth": (0.5, 1.0)}], {"cent": "cent.rvrn"}),
    # ...     ([{"wght": (0.5, 1.0)}], {"dollar": "dollar.rvrn"}),
    # ... ]
    # >>> addFeatureVariations(f, condSubst)
    # >>> f.save(dstPath)

    The `featureTag` parameter takes either a str or a iterable of str (the single str
    is kept for backwards compatibility), and defines which feature(s) will be
    associated with the feature variations.
    Note, if this is "rvrn", then the substitution lookup will be inserted at the
    beginning of the lookup list so that it is processed before others, otherwise
    for any other feature tags it will be appended last.
    """

    # process first when "rvrn" is the only listed tag
    featureTags = [featureTag] if isinstance(featureTag, str) else sorted(featureTag)
    processLast = "rvrn" not in featureTags or len(featureTags) > 1

    _checkSubstitutionGlyphsExist(
        glyphNames=set(font.getGlyphOrder()),
        substitutions=conditionalSubstitutions,
    )

    substitutions = overlayFeatureVariations(conditionalSubstitutions)

    # turn substitution dicts into tuples of tuples, so they are hashable
    conditionalSubstitutions, allSubstitutions = makeSubstitutionsHashable(
        substitutions
    )
    if "GSUB" not in font:
        font["GSUB"] = buildGSUB()
    else:
        existingTags = _existingVariableFeatures(font["GSUB"].table).intersection(
            featureTags
        )
        if existingTags:
            raise VarLibError(
                f"FeatureVariations already exist for feature tag(s): {existingTags}"
            )

    # setup lookups
    lookupMap = buildSubstitutionLookups(
        font["GSUB"].table, allSubstitutions, processLast
    )

    # addFeatureVariationsRaw takes a list of
    #  ( {condition}, [ lookup indices ] )
    # so rearrange our lookups to match
    conditionsAndLookups = []
    for conditionSet, substitutions in conditionalSubstitutions:
        conditionsAndLookups.append(
            (conditionSet, [lookupMap[s] for s in substitutions])
        )

    addFeatureVariationsRaw(font, font["GSUB"].table, conditionsAndLookups, featureTags)

    # Update OS/2.usMaxContext in case the font didn't have features before, but
    # does now, if the OS/2 table exists. The table may be required, but
    # fontTools needs to be able to deal with non-standard fonts. Since feature
    # variations are always 1:1 mappings, we can set the value to at least 1
    # instead of recomputing it with `otlLib.maxContextCalc.maxCtxFont()`.
    if (os2 := font.get("OS/2")) is not None:
        os2.usMaxContext = max(1, os2.usMaxContext)

