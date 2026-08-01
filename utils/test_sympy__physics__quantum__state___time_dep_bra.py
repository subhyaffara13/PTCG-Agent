
def test_sympy__physics__quantum__state__TimeDepBra():
    from sympy.physics.quantum.state import TimeDepBra
    assert _test_args(TimeDepBra('psi', 't'))

