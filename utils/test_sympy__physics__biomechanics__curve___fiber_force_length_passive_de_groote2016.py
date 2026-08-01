
def test_sympy__physics__biomechanics__curve__FiberForceLengthPassiveDeGroote2016():
    from sympy.physics.biomechanics import FiberForceLengthPassiveDeGroote2016
    l_M_tilde, c0, c1 = symbols('l_M_tilde, c0, c1')
    assert _test_args(FiberForceLengthPassiveDeGroote2016(l_M_tilde, c0, c1))

