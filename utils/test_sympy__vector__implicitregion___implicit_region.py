
def test_sympy__vector__implicitregion__ImplicitRegion():
    from sympy.vector.implicitregion import ImplicitRegion
    from sympy.abc import x, y
    assert _test_args(ImplicitRegion((x, y), y**3 - 4*x))

