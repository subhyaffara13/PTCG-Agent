
def test_erfcinv():
    assert erfcinv(1) is S.Zero
    assert erfcinv(0) is S.Infinity
    assert erfcinv(0, evaluate=False).is_infinite is True
    assert erfcinv(2, evaluate=False).is_infinite is True
    assert erfcinv(nan) is S.NaN

    assert erfcinv(x).diff() == -sqrt(pi)*exp(erfcinv(x)**2)/2
    raises(ArgumentIndexError, lambda: erfcinv(x).fdiff(2))

    assert erfcinv(z).rewrite('erfinv') == erfinv(1-z)
    assert erfcinv(z).inverse() == erfc

