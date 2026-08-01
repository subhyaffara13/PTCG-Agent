
def test_PolynomialRingBase():
    from sympy.polys.domains import QQ
    assert latex(QQ.old_poly_ring(x, y)) == r"\mathbb{Q}\left[x, y\right]"
    assert latex(QQ.old_poly_ring(x, y, order="ilex")) == \
        r"S_<^{-1}\mathbb{Q}\left[x, y\right]"


def test_PolynomialRingBase():
    assert srepr(ZZ.old_poly_ring(x)) == \
        "GlobalPolynomialRing(ZZ, Symbol('x'))"
    assert srepr(ZZ[x].old_poly_ring(y)) == \
        "GlobalPolynomialRing(ZZ[x], Symbol('y'))"
    assert srepr(QQ.frac_field(x).old_poly_ring(y)) == \
        "GlobalPolynomialRing(FractionField(FracField((Symbol('x'),), QQ, lex)), Symbol('y'))"

