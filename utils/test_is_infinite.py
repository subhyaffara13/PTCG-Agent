
def test_is_infinite():
    x = Symbol('x', infinite=True)
    y = Symbol('y', infinite=False)
    z = Symbol('z')
    assert is_infinite(x)
    assert not is_infinite(y)
    assert is_infinite(z) is None
    assert is_infinite(z, Q.infinite(z))

