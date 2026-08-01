
def _sort_systems(systems: Iterable[Iterable[Poly]]) -> list[list[Poly]]:
    """Sorts a list of lists of polynomials"""
    systems_list = [sorted(s, key=_poly_sort_key, reverse=True) for s in systems]
    return sorted(systems_list, key=_sys_sort_key, reverse=True)

