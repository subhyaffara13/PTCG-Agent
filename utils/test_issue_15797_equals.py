
def test_issue_15797_equals():
    Ri = 0.024127189424130748
    Ci = (0.0864931002830291, 0.0819863295239654)
    A = Point(0, 0.0578591400998346)
    c = Circle(Ci, Ri)  # evaluated
    assert c.is_tangent(c.tangent_lines(A)[0]) == True
    assert c.center.x.is_Rational
    assert c.center.y.is_Rational
    assert c.radius.is_Rational
    u = Circle(Ci, Ri, evaluate=False)  # unevaluated
    assert u.center.x.is_Float
    assert u.center.y.is_Float
    assert u.radius.is_Float

