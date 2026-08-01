
def test_tanh_fdiff():
    x = Symbol('x')
    raises(ArgumentIndexError, lambda: tanh(x).fdiff(2))

