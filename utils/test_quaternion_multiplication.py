
def test_quaternion_multiplication():
    q1 = Quaternion(3 + 4*I, 2 + 5*I, 0, 7 + 8*I, real_field = False)
    q2 = Quaternion(1, 2, 3, 5)
    q3 = Quaternion(1, 1, 1, y)

    assert Quaternion._generic_mul(S(4), S.One) == 4
    assert (Quaternion._generic_mul(S(4), q1) ==
            Quaternion(12 + 16*I, 8 + 20*I, 0, 28 + 32*I))
    assert q2.mul(2) == Quaternion(2, 4, 6, 10)
    assert q2.mul(q3) == Quaternion(-5*y - 4, 3*y - 2, 9 - 2*y, y + 4)
    assert q2.mul(q3) == q2*q3

    z = symbols('z', complex=True)
    z_quat = Quaternion(re(z), im(z), 0, 0)
    q = Quaternion(*symbols('q:4', real=True))

    assert z * q == z_quat * q
    assert q * z == q * z_quat

