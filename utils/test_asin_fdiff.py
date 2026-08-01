
def test_asin_fdiff():
    assert asin(x).fdiff() == 1/sqrt(1 - x**2)
    raises(ArgumentIndexError, lambda: asin(x).fdiff(2))

