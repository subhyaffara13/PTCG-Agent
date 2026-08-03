from typing import List

def sorted_specifiers(specifier: SpecifierSet) -> List[str]:
    """
    Return a list of sorted Specificier from a SpecifierSet, each converted to a
    string.
    The sort is done by version, then operator
    """
    by_version =  lambda spec: (_as_version(spec.version), spec.version, spec.operator)
    return [str(s) for s in sorted(specifier or [], key=by_version)]

