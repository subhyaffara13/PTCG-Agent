
def test_minpoly_fraction_field_slow():
    assert minimal_polynomial(minimal_polynomial(sqrt(x**Rational(1,5) - 1),
        y).subs(y, sqrt(x**Rational(1,5) - 1)), z) == z

