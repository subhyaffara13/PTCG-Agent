
def test_sympy__physics__control__lti__PIDController():
    from sympy.physics.control.lti import PIDController
    kp, ki, kd, tf = 1, 0.1, 0.01, 0
    assert _test_args_PIDController(PIDController(kp, ki, kd, tf, s))

