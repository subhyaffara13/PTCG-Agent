
def test_atan_fdiff():
    assert atan(x).fdiff() == 1/(x**2 + 1)
    raises(ArgumentIndexError, lambda: atan(x).fdiff(2))

