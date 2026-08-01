
def test_sympy__physics__biomechanics__curve__FiberForceLengthPassiveInverseDeGroote2016():
    from sympy.physics.biomechanics import FiberForceLengthPassiveInverseDeGroote2016
    fl_M_pas, c0, c1 = symbols('fl_M_pas, c0, c1')
    assert _test_args(FiberForceLengthPassiveInverseDeGroote2016(fl_M_pas, c0, c1))

