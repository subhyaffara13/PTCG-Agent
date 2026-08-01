
def test_sympy__physics__biomechanics__curve__FiberForceLengthActiveDeGroote2016():
    from sympy.physics.biomechanics import FiberForceLengthActiveDeGroote2016
    l_M_tilde, c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11 = symbols('l_M_tilde, c0:12')
    assert _test_args(FiberForceLengthActiveDeGroote2016(l_M_tilde, c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11))

