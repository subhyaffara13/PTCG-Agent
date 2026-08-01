
def test_Mul_is_rational():
    x = Symbol('x')
    n = Symbol('n', integer=True)
    m = Symbol('m', integer=True, nonzero=True)

    assert (n/m).is_rational is True
    assert (x/pi).is_rational is None
    assert (x/n).is_rational is None
    assert (m/pi).is_rational is False

    r = Symbol('r', rational=True)
    assert (pi*r).is_rational is None

    # issue 8008
    z = Symbol('z', zero=True)
    i = Symbol('i', imaginary=True)
    assert (z*i).is_rational is True
    bi = Symbol('i', imaginary=True, finite=True)
    assert (z*bi).is_zero is True

