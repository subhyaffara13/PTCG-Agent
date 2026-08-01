
def test_quaternion_evalf():
    assert (Quaternion(sqrt(2), 0, 0, sqrt(3)).evalf() ==
            Quaternion(sqrt(2).evalf(), 0, 0, sqrt(3).evalf()))
    assert (Quaternion(1/sqrt(2), 0, 0, 1/sqrt(2)).evalf() ==
            Quaternion((1/sqrt(2)).evalf(), 0, 0, (1/sqrt(2)).evalf()))

