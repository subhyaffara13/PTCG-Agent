
def test_sympy__geometry__line__Ray3D():
    from sympy.geometry.line import Ray3D
    assert _test_args(Ray3D((0, 1, 1), (2, 3, 4)))

