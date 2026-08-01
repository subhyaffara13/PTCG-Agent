
def test_union_types():
    @dispatch((A, C))
    def f(x): # noqa:F811
        return 1

    assert f(A()) == 1
    assert f(C()) == 1


def test_union_types():
    f = Dispatcher('f')
    f.register((int, float))(inc)

    assert f(1) == 2
    assert f(1.0) == 2.0

