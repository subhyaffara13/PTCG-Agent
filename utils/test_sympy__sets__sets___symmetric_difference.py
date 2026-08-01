
def test_sympy__sets__sets__SymmetricDifference():
    from sympy.sets.sets import FiniteSet, SymmetricDifference
    assert _test_args(SymmetricDifference(FiniteSet(1, 2, 3), \
           FiniteSet(2, 3, 4)))

