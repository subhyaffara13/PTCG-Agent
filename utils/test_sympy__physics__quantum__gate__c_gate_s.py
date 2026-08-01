
def test_sympy__physics__quantum__gate__CGateS():
    from sympy.physics.quantum.gate import CGateS, Gate
    assert _test_args(CGateS((0, 1), Gate(2)))

