
def test_sympy__stats__rv__ConditionalDomain():
    from sympy.stats.rv import ConditionalDomain, RandomDomain
    from sympy.sets.sets import FiniteSet
    D = RandomDomain(FiniteSet(x), FiniteSet(1, 2))
    assert _test_args(ConditionalDomain(D, x > 1))

