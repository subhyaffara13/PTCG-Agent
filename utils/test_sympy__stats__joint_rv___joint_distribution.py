
def test_sympy__stats__joint_rv__JointDistribution():
    from sympy.stats.joint_rv import JointDistribution
    assert _test_args(JointDistribution(1, 2, 3, 4))

