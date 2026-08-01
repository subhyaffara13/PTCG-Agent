
def test_sympy__geometry__ellipse__Circle():
    from sympy.geometry.ellipse import Circle
    assert _test_args(Circle((0, 1), 2))

