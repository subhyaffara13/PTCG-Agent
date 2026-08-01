
def test_sympy__stats__drv__DiscretePSpace():
    from sympy.stats.drv import DiscretePSpace, SingleDiscreteDomain
    density = Lambda(x, 2**(-x))
    domain = SingleDiscreteDomain(x, S.Naturals)
    assert _test_args(DiscretePSpace(domain, density))

