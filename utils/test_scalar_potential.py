
def test_scalar_potential():
    assert scalar_potential(Vector.zero, C) == 0
    assert scalar_potential(i, C) == x
    assert scalar_potential(j, C) == y
    assert scalar_potential(k, C) == z
    assert scalar_potential(y*z*i + x*z*j + x*y*k, C) == x*y*z
    assert scalar_potential(grad_field, C) == scalar_field
    assert scalar_potential(z*P.i + P.x*k, C) == x*z*cos(q) + y*z*sin(q)
    assert scalar_potential(z*P.i + P.x*k, P) == P.x*P.z
    raises(ValueError, lambda: scalar_potential(x*j, C))


def test_scalar_potential():
    assert scalar_potential(0, R) == 0
    assert scalar_potential(R.x, R) == R[0]
    assert scalar_potential(R.y, R) == R[1]
    assert scalar_potential(R.z, R) == R[2]
    assert scalar_potential(R[1]*R[2]*R.x + R[0]*R[2]*R.y + \
                            R[0]*R[1]*R.z, R) == R[0]*R[1]*R[2]
    assert scalar_potential(grad_field, R) == scalar_field
    assert scalar_potential(R[2]*P.x + P[0]*R.z, R) == \
           R[0]*R[2]*cos(q) + R[1]*R[2]*sin(q)
    assert scalar_potential(R[2]*P.x + P[0]*R.z, P) == P[0]*P[2]
    raises(ValueError, lambda: scalar_potential(R[0] * R.y, R))

