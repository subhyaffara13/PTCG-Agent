
def test_sympy__stats__rv__PSpace():
    from sympy.stats.rv import PSpace, RandomDomain
    from sympy.sets.sets import FiniteSet
    D = RandomDomain(FiniteSet(x), FiniteSet(1, 2, 3, 4, 5, 6))
    assert _test_args(PSpace(D, die))

