
def test_acoth_fdiff():
    x = Symbol('x')
    raises(ArgumentIndexError, lambda: acoth(x).fdiff(2))

