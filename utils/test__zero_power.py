
def test_Zero_power():
    z1 = ZeroMatrix(n, n)
    assert z1**4 == z1
    raises(ValueError, lambda:z1**-2)
    assert z1**0 == Identity(n)
    assert MatPow(z1, 2).doit() == z1**2
    raises(ValueError, lambda:MatPow(z1, -2).doit())
    z2 = ZeroMatrix(3, 3)
    assert MatPow(z2, 4).doit() == z2**4
    raises(ValueError, lambda:z2**-3)
    assert z2**3 == MatPow(z2, 3).doit()
    assert z2**0 == Identity(3)
    raises(ValueError, lambda:MatPow(z2, -1).doit())

