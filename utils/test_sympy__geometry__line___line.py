
def test_sympy__geometry__line__Line():
    from sympy.geometry.line import Line
    assert _test_args(Line((0, 1), (2, 3)))

