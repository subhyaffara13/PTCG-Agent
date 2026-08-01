
def test_sympy__physics__quantum__cartesian__PxKet():
    from sympy.physics.quantum.cartesian import PxKet
    assert _test_args(PxKet(x, y, z))

