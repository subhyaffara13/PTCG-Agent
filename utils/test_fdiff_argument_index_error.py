
def test_fdiff_argument_index_error():
    from sympy.core.function import ArgumentIndexError

    class myfunc(Function):
        nargs = 1  # define since there is no eval routine

        def fdiff(self, idx):
            raise ArgumentIndexError
    mf = myfunc(x)
    assert mf.diff(x) == Derivative(mf, x)
    raises(TypeError, lambda: myfunc(x, x))

