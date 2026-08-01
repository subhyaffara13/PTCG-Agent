
def test_sympy__physics__quantum__state__TimeDepState():
    from sympy.physics.quantum.state import TimeDepState
    assert _test_args(TimeDepState('psi', 't'))

