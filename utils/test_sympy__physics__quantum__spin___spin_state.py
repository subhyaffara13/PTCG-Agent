
def test_sympy__physics__quantum__spin__SpinState():
    from sympy.physics.quantum.spin import SpinState
    assert _test_args(SpinState(1, 0))

