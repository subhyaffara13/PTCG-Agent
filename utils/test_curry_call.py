
def test_curry_call():
    @curry
    def add(x, y):
        return x + y
    assert raises(TypeError, lambda: add.call(1))
    assert add(1)(2) == add.call(1, 2)
    assert add(1)(2) == add(1).call(2)

