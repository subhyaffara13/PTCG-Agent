
def test_asech_fdiff():
    x = Symbol('x')
    raises(ArgumentIndexError, lambda: asech(x).fdiff(2))

