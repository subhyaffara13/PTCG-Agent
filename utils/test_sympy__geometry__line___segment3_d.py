
def test_sympy__geometry__line__Segment3D():
    from sympy.geometry.line import Segment3D
    assert _test_args(Segment3D((0, 1, 1), (2, 3, 4)))

