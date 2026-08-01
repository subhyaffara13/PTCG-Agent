
def test_inheritance_and_multiple_dispatch():
    @dispatch(A, A)
    def f(x, y): # noqa:F811
        return type(x), type(y)

    @dispatch(A, B) # noqa:F811
    def f(x, y): # noqa:F811
        return 0

    assert f(A(), A()) == (A, A)
    assert f(A(), C()) == (A, C)
    assert f(A(), B()) == 0
    assert f(C(), B()) == 0
    assert raises(NotImplementedError, lambda: f(B(), B()))

