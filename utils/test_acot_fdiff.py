
def test_acot_fdiff():
    assert acot(x).fdiff() == -1/(x**2 + 1)
    raises(ArgumentIndexError, lambda: acot(x).fdiff(2))

