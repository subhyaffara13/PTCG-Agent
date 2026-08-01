
def test_make_func():
    f = make_func('')
    assert raises(ValueError, lambda: f())
    assert raises(TypeError, lambda: f(1))

    f = make_func('', raise_if_called=False)
    assert f()
    assert raises(TypeError, lambda: f(1))

    f = make_func('x, y=1', raise_if_called=False)
    assert f(1)
    assert f(x=1)
    assert f(1, 2)
    assert f(x=1, y=2)
    assert raises(TypeError, lambda: f(1, 2, 3))

    f = make_func('(x, y=1)', raise_if_called=False)
    assert f(1)
    assert f(x=1)
    assert f(1, 2)
    assert f(x=1, y=2)
    assert raises(TypeError, lambda: f(1, 2, 3))

