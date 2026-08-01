
def test_competing_multiple():
    @dispatch(A, B)
    def h(x, y): # noqa:F811
        return 1

    @dispatch(C, B) # noqa:F811
    def h(x, y): # noqa:F811
        return 2

    assert h(D(), B()) == 2

