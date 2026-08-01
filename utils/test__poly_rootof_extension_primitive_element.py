
def test_Poly_rootof_extension_primitive_element():
    r1 = rootof(x**3 + x + 3, 0)
    r2 = rootof(x**3 + x + 3, 1)
    K12 = QQ.algebraic_field(r1 + r2)
    assert Poly(r1*y + r2, y, extension=True) == Poly(r1*y + r2, y, domain=K12)

