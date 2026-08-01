
def test_sympy__geometry__plane__Plane():
    from sympy.geometry.plane import Plane
    assert _test_args(Plane((1, 1, 1), (-3, 4, -2), (1, 2, 3)))

