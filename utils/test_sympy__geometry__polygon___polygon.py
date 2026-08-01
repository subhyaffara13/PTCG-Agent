
def test_sympy__geometry__polygon__Polygon():
    from sympy.geometry.polygon import Polygon
    assert _test_args(Polygon((0, 1), (2, 3), (4, 5), (6, 7)))

