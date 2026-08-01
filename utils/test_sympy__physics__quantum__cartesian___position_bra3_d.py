
def test_sympy__physics__quantum__cartesian__PositionBra3D():
    from sympy.physics.quantum.cartesian import PositionBra3D
    assert _test_args(PositionBra3D(x, y, z))

