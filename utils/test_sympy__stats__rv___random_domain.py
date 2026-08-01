
def test_sympy__stats__rv__RandomDomain():
    from sympy.stats.rv import RandomDomain
    from sympy.sets.sets import FiniteSet
    assert _test_args(RandomDomain(FiniteSet(x), FiniteSet(1, 2, 3)))

