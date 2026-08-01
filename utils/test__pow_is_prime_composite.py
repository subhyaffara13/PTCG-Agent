
def test_Pow_is_prime_composite():
    x = Symbol('x', positive=True, integer=True)
    y = Symbol('y', positive=True, integer=True)
    assert (x**y).is_prime is None
    assert ( x**(y+1) ).is_prime is False
    assert ( x**(y+1) ).is_composite is None
    assert ( (x+1)**(y+1) ).is_composite is True
    assert ( (-x-1)**(2*y) ).is_composite is True

    x = Symbol('x', positive=True)
    assert (x**y).is_prime is None

