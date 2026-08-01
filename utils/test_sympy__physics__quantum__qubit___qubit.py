
def test_sympy__physics__quantum__qubit__Qubit():
    from sympy.physics.quantum.qubit import Qubit
    assert _test_args(Qubit(0, 0, 0))

