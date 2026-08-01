
def test_PolyRing_is_():
    R = PolyRing("x", QQ, lex)

    assert R.is_univariate is True
    assert R.is_multivariate is False

    R = PolyRing("x,y,z", QQ, lex)

    assert R.is_univariate is False
    assert R.is_multivariate is True

    R = PolyRing("", QQ, lex)

    assert R.is_univariate is False
    assert R.is_multivariate is False

