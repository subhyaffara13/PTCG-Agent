
def test_erfinv():
    assert erfinv(0) is S.Zero
    assert erfinv(1) is S.Infinity
    assert erfinv(nan) is S.NaN
    assert erfinv(-1) is S.NegativeInfinity

    assert erfinv(erf(w)) == w
    assert erfinv(erf(-w)) == -w

    assert erfinv(x).diff() == sqrt(pi)*exp(erfinv(x)**2)/2
    raises(ArgumentIndexError, lambda: erfinv(x).fdiff(2))

    assert erfinv(z).rewrite('erfcinv') == erfcinv(1-z)
    assert erfinv(z).inverse() == erf

