
def test_Poly_rootof_same_symbol_issue_26808():
    # XXX: This fails because r1 contains x.
    r1 = rootof(x**3 + x + 3, 0)
    K1 = QQ.algebraic_field(r1)
    assert Poly(r1, x) == Poly(r1, x, domain=EX)
    assert Poly(r1, x, extension=True) == Poly(r1, x, domain=K1)

