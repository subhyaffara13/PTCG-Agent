
def test_sympy__stats__joint_rv_types__JointDistributionHandmade():
    from sympy.tensor.indexed import Indexed
    from sympy.stats.joint_rv_types import JointDistributionHandmade
    x1, x2 = (Indexed('x', i) for i in (1, 2))
    assert _test_args(JointDistributionHandmade(x1 + x2, S.Reals**2))

