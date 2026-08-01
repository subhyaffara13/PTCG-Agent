
def test_Add_Mul_is_finite():
    x = Symbol('x', extended_real=True, finite=False)

    assert sin(x).is_finite is True
    assert (x*sin(x)).is_finite is None
    assert (x*atan(x)).is_finite is False
    assert (1024*sin(x)).is_finite is True
    assert (sin(x)*exp(x)).is_finite is None
    assert (sin(x)*cos(x)).is_finite is True
    assert (x*sin(x)*exp(x)).is_finite is None

    assert (sin(x) - 67).is_finite is True
    assert (sin(x) + exp(x)).is_finite is not True
    assert (1 + x).is_finite is False
    assert (1 + x**2 + (1 + x)*(1 - x)).is_finite is None
    assert (sqrt(2)*(1 + x)).is_finite is False
    assert (sqrt(2)*(1 + x)*(1 - x)).is_finite is False

