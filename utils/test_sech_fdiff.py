
def test_sech_fdiff():
    x = Symbol('x')
    raises(ArgumentIndexError, lambda: sech(x).fdiff(2))

