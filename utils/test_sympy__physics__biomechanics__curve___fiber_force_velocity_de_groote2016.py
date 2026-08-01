
def test_sympy__physics__biomechanics__curve__FiberForceVelocityDeGroote2016():
    from sympy.physics.biomechanics import FiberForceVelocityDeGroote2016
    v_M_tilde, c0, c1, c2, c3 = symbols('v_M_tilde, c0, c1, c2, c3')
    assert _test_args(FiberForceVelocityDeGroote2016(v_M_tilde, c0, c1, c2, c3))

