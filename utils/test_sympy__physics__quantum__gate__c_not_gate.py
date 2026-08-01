
def test_sympy__physics__quantum__gate__CNotGate():
    from sympy.physics.quantum.gate import CNotGate
    assert _test_args(CNotGate(0, 1))

