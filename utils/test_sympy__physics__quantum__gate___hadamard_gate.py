
def test_sympy__physics__quantum__gate__HadamardGate():
    from sympy.physics.quantum.gate import HadamardGate
    assert _test_args(HadamardGate(0))

