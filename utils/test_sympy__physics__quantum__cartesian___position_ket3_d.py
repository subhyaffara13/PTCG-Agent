
def test_sympy__physics__quantum__cartesian__PositionKet3D():
    from sympy.physics.quantum.cartesian import PositionKet3D
    assert _test_args(PositionKet3D(x, y, z))

