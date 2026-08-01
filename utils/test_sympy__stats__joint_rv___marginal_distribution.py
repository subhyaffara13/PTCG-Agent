
def test_sympy__stats__joint_rv__MarginalDistribution():
    from sympy.stats.rv import RandomSymbol
    from sympy.stats.joint_rv import MarginalDistribution
    r = RandomSymbol(S('r'))
    assert _test_args(MarginalDistribution(r, (r,)))

