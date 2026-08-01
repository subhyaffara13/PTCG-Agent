
def test_quaternion_construction_norm():
    q1 = Quaternion(*symbols('a:d'))

    q2 = Quaternion(w, x, y, z)
    assert expand((q1*q2).norm()**2 - (q1.norm()**2 * q2.norm()**2)) == 0

    q3 = Quaternion(w, x, y, z, norm=1)
    assert (q1 * q3).norm() == q1.norm()

