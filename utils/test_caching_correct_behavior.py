
def test_caching_correct_behavior():
    @dispatch(A)
    def f(x): # noqa:F811
        return 1

    assert f(C()) == 1

    @dispatch(C)
    def f(x): # noqa:F811
        return 2

    assert f(C()) == 2

