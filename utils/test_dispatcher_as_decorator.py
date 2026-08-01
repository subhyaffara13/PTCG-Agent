
def test_dispatcher_as_decorator():
    f = Dispatcher('f')

    @f.register(int)
    def inc(x): # noqa:F811
        return x + 1

    @f.register(float) # noqa:F811
    def inc(x): # noqa:F811
        return x - 1

    assert f(1) == 2
    assert f(1.0) == 0.0

