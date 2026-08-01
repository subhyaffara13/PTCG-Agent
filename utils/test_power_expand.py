
def test_power_expand():
    """Test for Pow.expand()"""
    a = Symbol('a')
    b = Symbol('b')
    p = (a + b)**2
    assert p.expand() == a**2 + b**2 + 2*a*b

    p = (1 + 2*(1 + a))**2
    assert p.expand() == 9 + 4*(a**2) + 12*a

    p = 2**(a + b)
    assert p.expand() == 2**a*2**b

    A = Symbol('A', commutative=False)
    B = Symbol('B', commutative=False)
    assert (2**(A + B)).expand() == 2**(A + B)
    assert (A**(a + b)).expand() != A**(a + b)

