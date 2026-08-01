
def test_Poly_LM_custom_order():
    f = Poly(x**2*y**3*z + x**2*y*z**3 + x*y*z + 1)
    rev_lex = lambda monom: tuple(reversed(monom))

    assert f.LM(order='lex') == (2, 3, 1)
    assert f.LM(order=rev_lex) == (2, 1, 3)

