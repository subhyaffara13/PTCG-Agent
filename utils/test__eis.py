
def test__eis():
    assert _eis(z).diff(z) == -_eis(z) + 1/z

    assert _eis(1/z).series(z) == \
        z + z**2 + 2*z**3 + 6*z**4 + 24*z**5 + O(z**6)

    assert Ei(z).rewrite('tractable') == exp(z)*_eis(z)
    assert li(z).rewrite('tractable') == z*_eis(log(z))

    assert _eis(z).rewrite('intractable') == exp(-z)*Ei(z)

    assert expand(li(z).rewrite('tractable').diff(z).rewrite('intractable')) \
        == li(z).diff(z)

    assert expand(Ei(z).rewrite('tractable').diff(z).rewrite('intractable')) \
        == Ei(z).diff(z)

    assert _eis(z).series(z, n=3) == EulerGamma + log(z) + z*(-log(z) - \
        EulerGamma + 1) + z**2*(log(z)/2 - Rational(3, 4) + EulerGamma/2)\
        + O(z**3*log(z))
    raises(ArgumentIndexError, lambda: _eis(z).fdiff(2))

