
def test_sympy__geometry__line__Segment2D():
    from sympy.geometry.line import Segment2D
    assert _test_args(Segment2D((0, 1), (2, 3)))

