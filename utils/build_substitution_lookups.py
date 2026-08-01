
def buildSubstitutionLookups(gsub, allSubstitutions, processLast=False):
    """Build the lookups for the glyph substitutions, return a dict mapping
    the substitution to lookup indices."""

    # Insert lookups at the beginning of the lookup vector
    # https://github.com/googlefonts/fontmake/issues/950

    firstIndex = len(gsub.LookupList.Lookup) if processLast else 0
    lookupMap = {}
    for i, substitutionMap in enumerate(allSubstitutions):
        lookupMap[substitutionMap] = firstIndex + i

    if not processLast:
        # Shift all lookup indices in gsub by len(allSubstitutions)
        shift = len(allSubstitutions)
        visitor = ShifterVisitor(shift)
        visitor.visit(gsub.FeatureList.FeatureRecord)
        visitor.visit(gsub.LookupList.Lookup)

    for i, subst in enumerate(allSubstitutions):
        substMap = dict(subst)
        lookup = buildLookup([buildSingleSubstSubtable(substMap)])
        if processLast:
            gsub.LookupList.Lookup.append(lookup)
        else:
            gsub.LookupList.Lookup.insert(i, lookup)
        assert gsub.LookupList.Lookup[lookupMap[subst]] is lookup
    gsub.LookupList.LookupCount = len(gsub.LookupList.Lookup)
    return lookupMap

