
def test_tan_fdiff():
    assert tan(x).fdiff() == tan(x)**2 + 1
    raises(ArgumentIndexError, lambda: tan(x).fdiff(2))

