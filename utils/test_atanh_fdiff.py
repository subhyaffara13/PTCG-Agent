
def test_atanh_fdiff():
    x = Symbol('x')
    raises(ArgumentIndexError, lambda: atanh(x).fdiff(2))

