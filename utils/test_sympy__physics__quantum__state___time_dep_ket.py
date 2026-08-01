
def test_sympy__physics__quantum__state__TimeDepKet():
    from sympy.physics.quantum.state import TimeDepKet
    assert _test_args(TimeDepKet('psi', 't'))

