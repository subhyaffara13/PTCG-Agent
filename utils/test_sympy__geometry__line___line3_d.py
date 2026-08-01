
def test_sympy__geometry__line__Line3D():
    from sympy.geometry.line import Line3D
    assert _test_args(Line3D((0, 1, 1), (2, 3, 4)))

