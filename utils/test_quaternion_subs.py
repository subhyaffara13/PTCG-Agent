
def test_quaternion_subs():
    q = Quaternion.from_axis_angle((0, 0, 1), phi)
    assert q.subs(phi, 0) == Quaternion(1, 0, 0, 0)

