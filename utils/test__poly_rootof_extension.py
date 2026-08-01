
def test_Poly_rootof_extension():
    r1 = rootof(x**3 + x + 3, 0)
    r2 = rootof(x**3 + x + 3, 1)
    K1 = QQ.algebraic_field(r1)
    K2 = QQ.algebraic_field(r2)
    assert Poly(r1, y) == Poly(r1, y, domain=EX)
    assert Poly(r2, y) == Poly(r2, y, domain=EX)
    assert Poly(r1, y, extension=True) == Poly(r1, y, domain=K1)
    assert Poly(r2, y, extension=True) == Poly(r2, y, domain=K2)

