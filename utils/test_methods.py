
def test_methods():
    class Foo:
        @dispatch(float)
        def f(self, x): # noqa:F811
            return x - 1

        @dispatch(int) # noqa:F811
        def f(self, x): # noqa:F811
            return x + 1

        @dispatch(int)
        def g(self, x): # noqa:F811
            return x + 3


    foo = Foo()
    assert foo.f(1) == 2
    assert foo.f(1.0) == 0.0
    assert foo.g(1) == 4


def test_methods(f, test_frame):
    g = test_frame.groupby("A")
    r = g.resample("2s")

    result = getattr(r, f)()
    expected = g.apply(lambda x: getattr(x.resample("2s"), f)())
    tm.assert_equal(result, expected)

