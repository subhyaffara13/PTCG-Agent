
def test_sympy__stats__joint_rv__JointPSpace():
    from sympy.stats.joint_rv import JointPSpace, JointDistribution
    assert _test_args(JointPSpace('X', JointDistribution(1)))

