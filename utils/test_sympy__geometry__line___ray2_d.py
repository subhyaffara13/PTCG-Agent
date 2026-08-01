
def test_sympy__geometry__line__Ray2D():
    from sympy.geometry.line import Ray2D
    assert _test_args(Ray2D((0, 1), (2, 3)))

