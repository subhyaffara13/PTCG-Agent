
def test_cosh_fdiff():
    x = Symbol('x')
    raises(ArgumentIndexError, lambda: cosh(x).fdiff(2))

