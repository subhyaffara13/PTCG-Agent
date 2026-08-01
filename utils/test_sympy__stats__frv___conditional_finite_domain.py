
def test_sympy__stats__frv__ConditionalFiniteDomain():
    from sympy.stats.frv import SingleFiniteDomain, ConditionalFiniteDomain
    xd = SingleFiniteDomain(x, {1, 2})
    assert _test_args(ConditionalFiniteDomain(xd, x > 1))

