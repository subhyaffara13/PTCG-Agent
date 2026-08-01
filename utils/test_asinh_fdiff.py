
def test_asinh_fdiff():
    x = Symbol('x')
    raises(ArgumentIndexError, lambda: asinh(x).fdiff(2))

