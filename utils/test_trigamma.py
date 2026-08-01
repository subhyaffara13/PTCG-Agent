
def test_trigamma():
    assert trigamma(nan) == nan

    assert trigamma(oo) == 0

    assert trigamma(1) == pi**2/6
    assert trigamma(2) == pi**2/6 - 1
    assert trigamma(3) == pi**2/6 - Rational(5, 4)

    assert trigamma(x, evaluate=False).rewrite(zeta) == zeta(2, x)
    assert trigamma(x, evaluate=False).rewrite(harmonic) == \
        trigamma(x).rewrite(polygamma).rewrite(harmonic)

    assert trigamma(x,evaluate=False).fdiff() == polygamma(2, x)

    assert trigamma(x,evaluate=False).is_real is None

    assert trigamma(x,evaluate=False).is_positive is None

    assert trigamma(x,evaluate=False).is_negative is None

    assert trigamma(x,evaluate=False).rewrite(polygamma) == polygamma(1, x)

