
def test_issue_17450():
    assert (erf(cosh(1)**7)**I).is_real is None
    assert (erf(cosh(1)**7)**I).is_imaginary is False
    assert (Pow(exp(1+sqrt(2)), ((1-sqrt(2))*I*pi), evaluate=False)).is_real is None
    assert ((-10)**(10*I*pi/3)).is_real is False
    assert ((-5)**(4*I*pi)).is_real is False

