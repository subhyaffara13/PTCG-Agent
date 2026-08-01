
def test_sympy__geometry__point__Point3D():
    from sympy.geometry.point import Point3D
    assert _test_args(Point3D(0, 1, 2))

