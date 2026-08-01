
def test_sympy__physics__quantum__qubit__QubitState():
    from sympy.physics.quantum.qubit import QubitState
    assert _test_args(QubitState(0, 1))

