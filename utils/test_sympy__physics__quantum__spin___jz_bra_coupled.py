
def test_sympy__physics__quantum__spin__JzBraCoupled():
    from sympy.physics.quantum.spin import JzBraCoupled
    assert _test_args(JzBraCoupled(1, 0, (1, 1)))

