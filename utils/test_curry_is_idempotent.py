
def test_curry_is_idempotent():
    def foo(a, b, c=1):
        return a + b + c

    f = curry(foo, 1, c=2)
    g = curry(f)
    assert isinstance(f, curry)
    assert isinstance(g, curry)
    assert not isinstance(g.func, curry)
    assert not hasattr(g.func, 'func')
    assert f.func == g.func
    assert f.args == g.args
    assert f.keywords == g.keywords

