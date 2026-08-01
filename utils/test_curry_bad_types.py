
def test_curry_bad_types():
    assert raises(TypeError, lambda: curry(1))

