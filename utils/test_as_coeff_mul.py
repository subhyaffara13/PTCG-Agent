
def test_as_coeff_mul():
    assert S(2).as_coeff_mul() == (2, ())
    assert S(3.0).as_coeff_mul() == (1, (S(3.0),))
    assert S(-3.0).as_coeff_mul() == (-1, (S(3.0),))
    assert S(-3.0).as_coeff_mul(rational=False) == (-S(3.0), ())
    assert x.as_coeff_mul() == (1, (x,))
    assert (-x).as_coeff_mul() == (-1, (x,))
    assert (2*x).as_coeff_mul() == (2, (x,))
    assert (x*y).as_coeff_mul(y) == (x, (y,))
    assert (3 + x).as_coeff_mul() == (1, (3 + x,))
    assert (3 + x).as_coeff_mul(y) == (3 + x, ())
    # don't do expansion
    e = exp(x + y)
    assert e.as_coeff_mul(y) == (1, (e,))
    e = 2**(x + y)
    assert e.as_coeff_mul(y) == (1, (e,))
    assert (1.1*x).as_coeff_mul(rational=False) == (1.1, (x,))
    assert (1.1*x).as_coeff_mul() == (1, (1.1, x))
    assert (-oo*x).as_coeff_mul(rational=True) == (-1, (oo, x))

