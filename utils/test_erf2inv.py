
def test_erf2inv():
    assert erf2inv(0, 0) is S.Zero
    assert erf2inv(0, 1) is S.Infinity
    assert erf2inv(1, 0) is S.One
    assert erf2inv(0, y) == erfinv(y)
    assert erf2inv(oo, y) == erfcinv(-y)
    assert erf2inv(x, 0) == x
    assert erf2inv(x, oo) == erfinv(x)
    assert erf2inv(nan, 0) is nan
    assert erf2inv(0, nan) is nan

    assert erf2inv(x, y).diff(x) == exp(-x**2 + erf2inv(x, y)**2)
    assert erf2inv(x, y).diff(y) == sqrt(pi)*exp(erf2inv(x, y)**2)/2
    raises(ArgumentIndexError, lambda: erf2inv(x, y).fdiff(3))

