
def test_singledispatch():
    @dispatch(int)
    def f(x): # noqa:F811
        return x + 1

    @dispatch(int)
    def g(x): # noqa:F811
        return x + 2

    @dispatch(float) # noqa:F811
    def f(x): # noqa:F811
        return x - 1

    assert f(1) == 2
    assert g(1) == 3
    assert f(1.0) == 0

    assert raises(NotImplementedError, lambda: f('hello'))

