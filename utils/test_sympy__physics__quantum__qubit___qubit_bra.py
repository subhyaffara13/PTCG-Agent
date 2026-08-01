
def test_sympy__physics__quantum__qubit__QubitBra():
    from sympy.physics.quantum.qubit import QubitBra
    assert _test_args(QubitBra('1', 0))

