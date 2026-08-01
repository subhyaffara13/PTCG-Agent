
def test_sympy__stats__joint_rv_types__MultivariateBetaDistribution():
    from sympy.stats.joint_rv_types import MultivariateBetaDistribution
    assert _test_args(MultivariateBetaDistribution([1, 2, 3]))

