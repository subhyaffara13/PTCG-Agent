
def test_sympy__sets__sets__FiniteSet():
    from sympy.sets.sets import FiniteSet
    assert _test_args(FiniteSet(x, y, z))

