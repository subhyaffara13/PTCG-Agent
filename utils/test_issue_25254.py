
def test_issue_25254():
    # calculating the inverse cached the norm which caused problems
    # when multiplying
    p = Quaternion(1, 0, 0, 0)
    q = Quaternion.from_axis_angle((1, 1, 1), 3 * math.pi/4)
    qi = q.inverse()  # this operation cached the norm
    test = q * p * qi
    assert ((test - p).norm() < 1E-10)

