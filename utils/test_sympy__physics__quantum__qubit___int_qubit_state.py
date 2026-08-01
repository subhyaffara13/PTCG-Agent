
def test_sympy__physics__quantum__qubit__IntQubitState():
    from sympy.physics.quantum.qubit import IntQubitState, QubitState
    assert _test_args(IntQubitState(QubitState(0, 1)))

