
def test_sympy__stats__drv__ConditionalDiscreteDomain():
    from sympy.stats.drv import ConditionalDiscreteDomain, SingleDiscreteDomain
    X = SingleDiscreteDomain(x, S.Naturals0)
    assert _test_args(ConditionalDiscreteDomain(X, x > 2))

