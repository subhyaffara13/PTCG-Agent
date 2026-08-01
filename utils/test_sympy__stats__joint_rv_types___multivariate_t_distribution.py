
def test_sympy__stats__joint_rv_types__MultivariateTDistribution():
    from sympy.stats.joint_rv_types import MultivariateTDistribution
    assert _test_args(MultivariateTDistribution([0, 1], [[1, 0],[0, 1]], 1))

