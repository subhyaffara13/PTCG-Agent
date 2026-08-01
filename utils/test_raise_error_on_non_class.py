
def test_raise_error_on_non_class():
    f = Dispatcher('f')
    assert raises(TypeError, lambda: f.add((1,), inc))

