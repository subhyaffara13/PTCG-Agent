
def test_sympy__physics__quantum__cartesian__PositionState3D():
    from sympy.physics.quantum.cartesian import PositionState3D
    assert _test_args(PositionState3D(x, y, z))

