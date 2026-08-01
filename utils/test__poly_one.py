
def test_Poly_one():
    assert Poly(x).one == Poly(1, x, domain=ZZ)
    assert Poly(x/2).one == Poly(1, x, domain=QQ)

