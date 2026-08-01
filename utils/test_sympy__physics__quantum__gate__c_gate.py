
def test_sympy__physics__quantum__gate__CGate():
    from sympy.physics.quantum.gate import CGate, Gate
    assert _test_args(CGate((0, 1), Gate(2)))

