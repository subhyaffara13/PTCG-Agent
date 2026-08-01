
def test_sympy__stats__frv__ProductFiniteDomain():
    from sympy.stats.frv import SingleFiniteDomain, ProductFiniteDomain
    xd = SingleFiniteDomain(x, {1, 2})
    yd = SingleFiniteDomain(y, {1, 2})
    assert _test_args(ProductFiniteDomain(xd, yd))

