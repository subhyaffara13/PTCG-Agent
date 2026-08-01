
def test_sin_fdiff():
    assert sin(x).fdiff() == cos(x)
    raises(ArgumentIndexError, lambda: sin(x).fdiff(2))

