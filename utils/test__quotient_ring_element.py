
def test_QuotientRingElement():
    R = QQ.old_poly_ring(x)/[x**10]
    X = R.convert(x)

    assert X*(X + 1) == R.convert(x**2 + x)
    assert X*x == R.convert(x**2)
    assert x*X == R.convert(x**2)
    assert X + x == R.convert(2*x)
    assert x + X == 2*X
    assert X**2 == R.convert(x**2)
    assert 1/(1 - X) == R.convert(sum(x**i for i in range(10)))
    assert X**10 == R.zero
    assert X != x

    raises(NotReversible, lambda: 1/X)

