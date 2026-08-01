
def test_sympy__geometry__line__Line2D():
    from sympy.geometry.line import Line2D
    assert _test_args(Line2D((0, 1), (2, 3)))

