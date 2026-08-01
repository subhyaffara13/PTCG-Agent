
def test_methods_multiple_dispatch():
    class Foo:
        @dispatch(A, A)
        def f(x, y): # noqa:F811
            return 1

        @dispatch(A, C) # noqa:F811
        def f(x, y): # noqa:F811
            return 2


    foo = Foo()
    assert foo.f(A(), A()) == 1
    assert foo.f(A(), C()) == 2
    assert foo.f(C(), C()) == 2

