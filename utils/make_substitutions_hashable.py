
def makeSubstitutionsHashable(conditionalSubstitutions):
    """Turn all the substitution dictionaries in sorted tuples of tuples so
    they are hashable, to detect duplicates so we don't write out redundant
    data."""
    allSubstitutions = set()
    condSubst = []
    for conditionSet, substitutionMaps in conditionalSubstitutions:
        substitutions = []
        for substitutionMap in substitutionMaps:
            subst = tuple(sorted(substitutionMap.items()))
            substitutions.append(subst)
            allSubstitutions.add(subst)
        condSubst.append((conditionSet, substitutions))
    return condSubst, sorted(allSubstitutions)

