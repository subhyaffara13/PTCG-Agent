
def test_sympy__stats__joint_rv_types__MultivariateEwensDistribution():
    from sympy.stats.joint_rv_types import MultivariateEwensDistribution
    assert _test_args(MultivariateEwensDistribution(5, 1))

