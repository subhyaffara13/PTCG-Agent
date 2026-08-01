
def test_curry_attributes_writable():
    def foo(a, b, c=1):
        return a + b + c
    foo.__qualname__ = 'this.is.foo'
    f = curry(foo, 1, c=2)
    assert f.__qualname__ == 'this.is.foo'
    f.__name__ = 'newname'
    f.__doc__ = 'newdoc'
    f.__module__ = 'newmodule'
    f.__qualname__ = 'newqualname'
    assert f.__name__ == 'newname'
    assert f.__doc__ == 'newdoc'
    assert f.__module__ == 'newmodule'
    assert f.__qualname__ == 'newqualname'
    if hasattr(f, 'func_name'):
        assert f.__name__ == f.func_name

