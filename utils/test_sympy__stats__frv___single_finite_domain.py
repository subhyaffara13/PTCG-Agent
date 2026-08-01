
def test_sympy__stats__frv__SingleFiniteDomain():
    from sympy.stats.frv import SingleFiniteDomain
    assert _test_args(SingleFiniteDomain(x, {1, 2}))  # x can be 1 or 2

