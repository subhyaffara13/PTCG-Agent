
def test_sympy__physics__quantum__spin__JxKetCoupled():
    from sympy.physics.quantum.spin import JxKetCoupled
    assert _test_args(JxKetCoupled(1, 0, (1, 1)))

