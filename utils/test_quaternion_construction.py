
def test_quaternion_construction():
    q = Quaternion(w, x, y, z)
    assert q + q == Quaternion(2*w, 2*x, 2*y, 2*z)

    q2 = Quaternion.from_axis_angle((sqrt(3)/3, sqrt(3)/3, sqrt(3)/3),
                                    pi*Rational(2, 3))
    assert q2 == Quaternion(S.Half, S.Half,
                            S.Half, S.Half)

    M = Matrix([[cos(phi), -sin(phi), 0], [sin(phi), cos(phi), 0], [0, 0, 1]])
    q3 = trigsimp(Quaternion.from_rotation_matrix(M))
    assert q3 == Quaternion(
        sqrt(2)*sqrt(cos(phi) + 1)/2, 0, 0, sqrt(2 - 2*cos(phi))*sign(sin(phi))/2)

    nc = Symbol('nc', commutative=False)
    raises(ValueError, lambda: Quaternion(w, x, nc, z))

