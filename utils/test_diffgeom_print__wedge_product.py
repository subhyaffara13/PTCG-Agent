
def test_diffgeom_print_WedgeProduct():
    from sympy.diffgeom.rn import R2
    from sympy.diffgeom import WedgeProduct
    wp = WedgeProduct(R2.dx, R2.dy)
    assert upretty(wp) == "ⅆ x∧ⅆ y"
    assert pretty(wp) == r"d x/\d y"

