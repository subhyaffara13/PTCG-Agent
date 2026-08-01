
def test_sympy__stats__joint_rv_types__MultivariateNormalDistribution():
    from sympy.stats.joint_rv_types import MultivariateNormalDistribution
    assert _test_args(
        MultivariateNormalDistribution([0, 1], [[1, 0],[0, 1]]))

