
def _sys_sort_key(sys):
    """Sort key for lists of polynomials"""
    return list(zip(*map(_poly_sort_key, sys)))

