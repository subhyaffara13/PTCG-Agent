
def test_curried_bad_qualname():
    @toolz.curry
    class Bad:
        __qualname__ = 'toolz.functoolz.not.a.valid.path'

    assert raises(pickle.PicklingError, lambda: pickle.dumps(Bad))

