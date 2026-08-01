
def test_sympy__polys__polytools__GroebnerBasis():
    from sympy.polys.polytools import GroebnerBasis
    assert _test_args(GroebnerBasis([x, y, z], x, y, z))

