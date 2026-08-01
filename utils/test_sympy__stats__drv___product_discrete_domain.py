
def test_sympy__stats__drv__ProductDiscreteDomain():
    from sympy.stats.drv import SingleDiscreteDomain, ProductDiscreteDomain
    X = SingleDiscreteDomain(x, S.Naturals)
    Y = SingleDiscreteDomain(y, S.Integers)
    assert _test_args(ProductDiscreteDomain(X, Y))

