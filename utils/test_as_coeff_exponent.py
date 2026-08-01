
def test_as_coeff_exponent():
    assert (3*x**4).as_coeff_exponent(x) == (3, 4)
    assert (2*x**3).as_coeff_exponent(x) == (2, 3)
    assert (4*x**2).as_coeff_exponent(x) == (4, 2)
    assert (6*x**1).as_coeff_exponent(x) == (6, 1)
    assert (3*x**0).as_coeff_exponent(x) == (3, 0)
    assert (2*x**0).as_coeff_exponent(x) == (2, 0)
    assert (1*x**0).as_coeff_exponent(x) == (1, 0)
    assert (0*x**0).as_coeff_exponent(x) == (0, 0)
    assert (-1*x**0).as_coeff_exponent(x) == (-1, 0)
    assert (-2*x**0).as_coeff_exponent(x) == (-2, 0)
    assert (2*x**3 + pi*x**3).as_coeff_exponent(x) == (2 + pi, 3)
    assert (x*log(2)/(2*x + pi*x)).as_coeff_exponent(x) == \
        (log(2)/(2 + pi), 0)
    # issue 4784
    D = Derivative
    fx = D(f(x), x)
    assert fx.as_coeff_exponent(f(x)) == (fx, 0)

