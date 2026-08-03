import sys

def _factor_sets_slow(eqs: list[list]) -> set[frozenset]:
    """
    Helper to find the minimal set of factorised subsystems that is
    equivalent to the original system.

    The result is in DNF.
    """
    if not eqs:
        return {frozenset()}
    systems_set = {frozenset(sys) for sys in cartes(*eqs)}
    return {s1 for s1 in systems_set if not any(s1 > s2 for s2 in systems_set)}

