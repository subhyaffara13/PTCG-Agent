
def test_sympy__physics__vector__frame__CoordinateSym():
    from sympy.physics.vector import CoordinateSym
    from sympy.physics.vector import ReferenceFrame
    assert _test_args(CoordinateSym('R_x', ReferenceFrame('R'), 0))

