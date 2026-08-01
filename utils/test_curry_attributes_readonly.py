
def test_curry_attributes_readonly():
    def foo(a, b, c=1):
        return a + b + c

    f = curry(foo, 1, c=2)
    assert raises(AttributeError, lambda: setattr(f, 'args', (2,)))
    assert raises(AttributeError, lambda: setattr(f, 'keywords', {'c': 3}))
    assert raises(AttributeError, lambda: setattr(f, 'func', f))
    assert raises(AttributeError, lambda: delattr(f, 'args'))
    assert raises(AttributeError, lambda: delattr(f, 'keywords'))
    assert raises(AttributeError, lambda: delattr(f, 'func'))

