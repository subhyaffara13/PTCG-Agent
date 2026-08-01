
def test_sympy__geometry__polygon__RegularPolygon():
    from sympy.geometry.polygon import RegularPolygon
    assert _test_args(RegularPolygon((0, 1), 2, 3, 4))

