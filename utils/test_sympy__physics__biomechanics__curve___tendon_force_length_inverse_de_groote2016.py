
def test_sympy__physics__biomechanics__curve__TendonForceLengthInverseDeGroote2016():
    from sympy.physics.biomechanics import TendonForceLengthInverseDeGroote2016
    fl_T, c0, c1, c2, c3 = symbols('fl_T, c0, c1, c2, c3')
    assert _test_args(TendonForceLengthInverseDeGroote2016(fl_T, c0, c1, c2, c3))

