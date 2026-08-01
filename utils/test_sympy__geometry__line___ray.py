
def test_sympy__geometry__line__Ray():
    from sympy.geometry.line import Ray
    assert _test_args(Ray((0, 1), (2, 3)))

