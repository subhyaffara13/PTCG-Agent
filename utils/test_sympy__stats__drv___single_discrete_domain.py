
def test_sympy__stats__drv__SingleDiscreteDomain():
    from sympy.stats.drv import SingleDiscreteDomain
    assert _test_args(SingleDiscreteDomain(x, S.Naturals))

