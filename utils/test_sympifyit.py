
def test_sympifyit():
    x = Symbol('x')
    y = Symbol('y')

    @_sympifyit('b', NotImplemented)
    def add(a, b):
        return a + b

    assert add(x, 1) == x + 1
    assert add(x, 0.5) == x + Float('0.5')
    assert add(x, y) == x + y

    assert add(x, '1') == NotImplemented

    @_sympifyit('b')
    def add_raises(a, b):
        return a + b

    assert add_raises(x, 1) == x + 1
    assert add_raises(x, 0.5) == x + Float('0.5')
    assert add_raises(x, y) == x + y

    raises(SympifyError, lambda: add_raises(x, '1'))

