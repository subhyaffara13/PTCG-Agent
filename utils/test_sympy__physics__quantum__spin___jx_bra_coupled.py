
def test_sympy__physics__quantum__spin__JxBraCoupled():
    from sympy.physics.quantum.spin import JxBraCoupled
    assert _test_args(JxBraCoupled(1, 0, (1, 1)))

