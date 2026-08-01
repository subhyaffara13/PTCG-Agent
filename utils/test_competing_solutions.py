
def test_competing_solutions():
    @dispatch(A)
    def h(x): # noqa:F811
        return 1

    @dispatch(C) # noqa:F811
    def h(x): # noqa:F811
        return 2

    assert h(D()) == 2

