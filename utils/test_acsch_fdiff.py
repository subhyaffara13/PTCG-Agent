
def test_acsch_fdiff():
    x = Symbol('x')
    raises(ArgumentIndexError, lambda: acsch(x).fdiff(2))

