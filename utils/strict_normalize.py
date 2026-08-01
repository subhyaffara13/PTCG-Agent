
def strict_normalize(sign, man, exp, bc, prec, rnd):
    """Additional checks on the components of an mpf. Enable tests by setting
       the environment variable MPMATH_STRICT to Y."""
    assert type(man) == MPZ_TYPE
    assert type(bc) in _exp_types
    assert type(exp) in _exp_types
    assert bc == bitcount(man)
    return _normalize(sign, man, exp, bc, prec, rnd)

