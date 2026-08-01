
def test_sympy__sets__sets__DisjointUnion():
    from sympy.sets.sets import FiniteSet, DisjointUnion
    assert _test_args(DisjointUnion(FiniteSet(1, 2, 3), \
           FiniteSet(2, 3, 4)))

