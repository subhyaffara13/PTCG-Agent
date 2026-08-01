
def test_sympy__physics__quantum__gate__OneQubitGate():
    from sympy.physics.quantum.gate import OneQubitGate
    assert _test_args(OneQubitGate(0))

