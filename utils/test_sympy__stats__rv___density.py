
def test_sympy__stats__rv__Density():
    from sympy.stats.rv import Density
    from sympy.stats.crv_types import Normal
    assert _test_args(Density(Normal('x', 0, 1)))

