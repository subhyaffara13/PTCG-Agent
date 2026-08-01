
def test_sympy__stats__rv__SingleDomain():
    from sympy.stats.rv import SingleDomain
    from sympy.sets.sets import FiniteSet
    assert _test_args(SingleDomain(x, FiniteSet(1, 2, 3)))

