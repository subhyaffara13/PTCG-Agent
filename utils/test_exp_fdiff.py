
def test_exp_fdiff():
    x = Symbol('x')
    raises(ArgumentIndexError, lambda: exp(x).fdiff(2))

