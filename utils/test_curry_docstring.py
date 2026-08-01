
def test_curry_docstring():
    def f(x, y):
        """ A docstring """
        return x

    g = curry(f)
    assert g.__doc__ == f.__doc__
    assert str(g) == str(f)
    assert f(1, 2) == g(1, 2)

