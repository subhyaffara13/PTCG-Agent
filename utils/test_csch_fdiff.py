
def test_csch_fdiff():
    x = Symbol('x')
    raises(ArgumentIndexError, lambda: csch(x).fdiff(2))

