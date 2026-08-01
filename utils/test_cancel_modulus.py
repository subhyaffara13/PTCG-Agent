
def test_cancel_modulus():
    assert cancel((x**2 - 1)/(x + 1), modulus=2) == x + 1
    assert Poly(x**2 - 1, modulus=2).cancel(Poly(x + 1, modulus=2)) ==\
            (1, Poly(x + 1, modulus=2), Poly(1, x, modulus=2))

