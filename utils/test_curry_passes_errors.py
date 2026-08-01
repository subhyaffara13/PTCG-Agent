
def test_curry_passes_errors():
    @curry
    def f(a, b):
        if not isinstance(a, int):
            raise TypeError()
        return a + b

    assert f(1, 2) == 3
    assert raises(TypeError, lambda: f('1', 2))
    assert raises(TypeError, lambda: f('1')(2))
    assert raises(TypeError, lambda: f(1, 2, 3))

