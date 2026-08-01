
def test_gcdex_diophantine():
    assert gcdex_diophantine(Poly(x**4 - 2*x**3 - 6*x**2 + 12*x + 15),
    Poly(x**3 + x**2 - 4*x - 4), Poly(x**2 - 1)) == \
        (Poly((-x**2 + 4*x - 3)/5), Poly((x**3 - 7*x**2 + 16*x - 10)/5))
    assert gcdex_diophantine(Poly(x**3 + 6*x + 7), Poly(x**2 + 3*x + 2), Poly(x + 1)) == \
        (Poly(1/13, x, domain='QQ'), Poly(-1/13*x + 3/13, x, domain='QQ'))

