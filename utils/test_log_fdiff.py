
def test_log_fdiff():
    x = Symbol('x')
    raises(ArgumentIndexError, lambda: log(x).fdiff(2))

