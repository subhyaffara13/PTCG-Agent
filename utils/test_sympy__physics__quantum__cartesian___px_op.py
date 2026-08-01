
def test_sympy__physics__quantum__cartesian__PxOp():
    from sympy.physics.quantum.cartesian import PxOp
    assert _test_args(PxOp(x, y, z))

