
def test_Poly_rootof_extension_to_sympy():
    # Verify that when primitive elements and RootOf are used, the expression
    # is not exploded on the way back to sympy.
    r1 = rootof(y**3 + y**2 - 1, 0)
    r2 = rootof(z**5 + z**2 - 1, 0)
    p = -x**5 + x**2 + x*r1 - r2 + 3*r1**2
    assert p.as_poly(x, extension=True).as_expr() == p

