
def test_sinh_fdiff():
    x = Symbol('x')
    raises(ArgumentIndexError, lambda: sinh(x).fdiff(2))

