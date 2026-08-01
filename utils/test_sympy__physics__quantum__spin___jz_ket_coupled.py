
def test_sympy__physics__quantum__spin__JzKetCoupled():
    from sympy.physics.quantum.spin import JzKetCoupled
    assert _test_args(JzKetCoupled(1, 0, (1, 1)))

