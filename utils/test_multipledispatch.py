
def test_multipledispatch():
    @dispatch(int, int)
    def f(x, y): # noqa:F811
        return x + y

    @dispatch(float, float) # noqa:F811
    def f(x, y): # noqa:F811
        return x - y

    assert f(1, 2) == 3
    assert f(1.0, 2.0) == -1.0

