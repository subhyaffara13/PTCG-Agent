
def test_sympy__physics__quantum__gate__SwapGate():
    from sympy.physics.quantum.gate import SwapGate
    assert _test_args(SwapGate(0, 1))

