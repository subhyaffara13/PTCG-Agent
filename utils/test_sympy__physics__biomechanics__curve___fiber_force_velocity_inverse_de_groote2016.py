
def test_sympy__physics__biomechanics__curve__FiberForceVelocityInverseDeGroote2016():
    from sympy.physics.biomechanics import FiberForceVelocityInverseDeGroote2016
    fv_M, c0, c1, c2, c3 = symbols('fv_M, c0, c1, c2, c3')
    assert _test_args(FiberForceVelocityInverseDeGroote2016(fv_M, c0, c1, c2, c3))

