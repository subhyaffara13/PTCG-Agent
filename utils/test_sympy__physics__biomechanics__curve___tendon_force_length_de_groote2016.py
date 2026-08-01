
def test_sympy__physics__biomechanics__curve__TendonForceLengthDeGroote2016():
    from sympy.physics.biomechanics import TendonForceLengthDeGroote2016
    l_T_tilde, c0, c1, c2, c3 = symbols('l_T_tilde, c0, c1, c2, c3')
    assert _test_args(TendonForceLengthDeGroote2016(l_T_tilde, c0, c1, c2, c3))

