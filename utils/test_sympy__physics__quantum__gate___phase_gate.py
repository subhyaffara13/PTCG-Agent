
def test_sympy__physics__quantum__gate__PhaseGate():
    from sympy.physics.quantum.gate import PhaseGate
    assert _test_args(PhaseGate(0))

