
def test_digamma():
    assert digamma(nan) == nan

    assert digamma(oo) == oo
    assert digamma(-oo) == oo
    assert digamma(I*oo) == oo
    assert digamma(-I*oo) == oo

    assert digamma(-9) == zoo

    assert digamma(-9) == zoo
    assert digamma(-1) == zoo

    assert digamma(0) == zoo

    assert digamma(1) == -EulerGamma
    assert digamma(7) == Rational(49, 20) - EulerGamma

    def t(m, n):
        x = S(m)/n
        r = digamma(x)
        if r.has(digamma):
            return False
        return abs(digamma(x.n()).n() - r.n()).n() < 1e-10
    assert t(1, 2)
    assert t(3, 2)
    assert t(-1, 2)
    assert t(1, 4)
    assert t(-3, 4)
    assert t(1, 3)
    assert t(4, 3)
    assert t(3, 4)
    assert t(2, 3)
    assert t(123, 5)

    assert digamma(x).rewrite(zeta) == polygamma(0, x)

    assert digamma(x).rewrite(harmonic) == harmonic(x - 1) - EulerGamma

    assert digamma(I).is_real is None

    assert digamma(x,evaluate=False).fdiff() == polygamma(1, x)

    assert digamma(x,evaluate=False).is_real is None

    assert digamma(x,evaluate=False).is_positive is None

    assert digamma(x,evaluate=False).is_negative is None

    assert digamma(x,evaluate=False).rewrite(polygamma) == polygamma(0, x)

