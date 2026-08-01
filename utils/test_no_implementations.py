
def test_no_implementations():
    f = Dispatcher('f')
    assert raises(NotImplementedError, lambda: f('hello'))

