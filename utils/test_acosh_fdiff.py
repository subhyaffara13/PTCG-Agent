
def test_acosh_fdiff():
    x = Symbol('x')
    raises(ArgumentIndexError, lambda: acosh(x).fdiff(2))

