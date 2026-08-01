
def test_curry_subclassable():
    class mycurry(curry):
        pass

    add = mycurry(lambda x, y: x+y)
    assert isinstance(add, curry)
    assert isinstance(add, mycurry)
    assert isinstance(add(1), mycurry)
    assert isinstance(add()(1), mycurry)
    assert add(1)(2) == 3

    # Should we make `_should_curry` public?
    """
    class curry2(curry):
        def _should_curry(self, args, kwargs, exc=None):
            return len(self.args) + len(args) < 2

    add = curry2(lambda x, y: x+y)
    assert isinstance(add(1), curry2)
    assert add(1)(2) == 3
    assert isinstance(add(1)(x=2), curry2)
    assert raises(TypeError, lambda: add(1)(x=2)(3))
    """

