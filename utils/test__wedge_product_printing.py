
def test_WedgeProduct_printing():
    from sympy.diffgeom.rn import R2
    from sympy.diffgeom import WedgeProduct
    wp = WedgeProduct(R2.dx, R2.dy)
    assert latex(wp) == r"\operatorname{d}x \wedge \operatorname{d}y"

