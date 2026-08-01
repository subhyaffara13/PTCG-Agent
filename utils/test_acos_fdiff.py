
def test_acos_fdiff():
    assert acos(x).fdiff() == -1/sqrt(1 - x**2)
    raises(ArgumentIndexError, lambda: acos(x).fdiff(2))

