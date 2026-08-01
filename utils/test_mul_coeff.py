
def test_mul_coeff():
    # It is important that all Numbers be removed from the seq;
    # This can be tricky when powers combine to produce those numbers
    p = exp(I*pi/3)
    assert p**2*x*p*y*p*x*p**2 == x**2*y

