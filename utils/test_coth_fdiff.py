
def test_coth_fdiff():
    x = Symbol('x')
    raises(ArgumentIndexError, lambda: coth(x).fdiff(2))

