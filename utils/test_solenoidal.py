
def test_solenoidal():
    assert is_solenoidal(Vector.zero) is True
    assert is_solenoidal(i) is True
    assert is_solenoidal(2 * i + 3 * j + 4 * k) is True
    assert (is_solenoidal(y*z*i + x*z*j + x*y*k) is
            True)
    assert is_solenoidal(y * j) is False
    assert is_solenoidal(grad_field) is False
    assert is_solenoidal(curl_field) is True
    assert is_solenoidal((-2*y + 3)*k) is True
    assert is_solenoidal(cos(q)*i + sin(q)*j + cos(q)*P.k) is True
    assert is_solenoidal(z*P.i + P.x*k) is True


def test_solenoidal():
    assert is_solenoidal(0) is True
    assert is_solenoidal(R.x) is True
    assert is_solenoidal(2 * R.x + 3 * R.y + 4 * R.z) is True
    assert is_solenoidal(R[1]*R[2]*R.x + R[0]*R[2]*R.y + R[0]*R[1]*R.z) is \
           True
    assert is_solenoidal(R[1] * R.y) is False
    assert is_solenoidal(grad_field) is False
    assert is_solenoidal(curl_field) is True
    assert is_solenoidal((-2*R[1] + 3)*R.z) is True
    assert is_solenoidal(cos(q)*R.x + sin(q)*R.y + cos(q)*P.z) is True
    assert is_solenoidal(R[2]*P.x + P[0]*R.z) is True

