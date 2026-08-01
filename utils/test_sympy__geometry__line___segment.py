
def test_sympy__geometry__line__Segment():
    from sympy.geometry.line import Segment
    assert _test_args(Segment((0, 1), (2, 3)))

