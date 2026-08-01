
def test_conservative():
    assert is_conservative(Vector.zero) is True
    assert is_conservative(i) is True
    assert is_conservative(2 * i + 3 * j + 4 * k) is True
    assert (is_conservative(y*z*i + x*z*j + x*y*k) is
            True)
    assert is_conservative(x * j) is False
    assert is_conservative(grad_field) is True
    assert is_conservative(curl_field) is False
    assert (is_conservative(4*x*y*z*i + 2*x**2*z*j) is
            False)
    assert is_conservative(z*P.i + P.x*k) is True


def test_conservative():
    assert is_conservative(0) is True
    assert is_conservative(R.x) is True
    assert is_conservative(2 * R.x + 3 * R.y + 4 * R.z) is True
    assert is_conservative(R[1]*R[2]*R.x + R[0]*R[2]*R.y + R[0]*R[1]*R.z) is \
           True
    assert is_conservative(R[0] * R.y) is False
    assert is_conservative(grad_field) is True
    assert is_conservative(curl_field) is False
    assert is_conservative(4*R[0]*R[1]*R[2]*R.x + 2*R[0]**2*R[2]*R.y) is \
                           False
    assert is_conservative(R[2]*P.x + P[0]*R.z) is True

