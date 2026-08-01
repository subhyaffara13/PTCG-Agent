
def test_sympy__stats__joint_rv_types__MultivariateLaplaceDistribution():
    from sympy.stats.joint_rv_types import MultivariateLaplaceDistribution
    assert _test_args(MultivariateLaplaceDistribution([0, 1], [[1, 0],[0, 1]]))

