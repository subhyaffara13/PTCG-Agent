
def N_equals(a, b):
    """Check whether two complex numbers are numerically close"""
    return comp(a.n(), b.n(), 1.e-6)

