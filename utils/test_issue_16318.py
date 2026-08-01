
def test_issue_16318():
    # test compute_expectation function of the SingleContinuousDomain
    N = SingleContinuousDomain(x, Interval(0, 1))
    raises(ValueError, lambda: SingleContinuousDomain.compute_expectation(N, x+1, {x, y}))


def test_issue_16318():
    #for rtruediv
    q0 = Quaternion(0, 0, 0, 0)
    raises(ValueError, lambda: 1/q0)
    #for rotate_point
    q = Quaternion(1, 2, 3, 4)
    (axis, angle) = q.to_axis_angle()
    assert Quaternion.rotate_point((1, 1, 1), (axis, angle)) == (S.One / 5, 1, S(7) / 5)
    #test for to_axis_angle
    q = Quaternion(-1, 1, 1, 1)
    axis = (-sqrt(3)/3, -sqrt(3)/3, -sqrt(3)/3)
    angle = 2*pi/3
    assert (axis, angle) == q.to_axis_angle()

