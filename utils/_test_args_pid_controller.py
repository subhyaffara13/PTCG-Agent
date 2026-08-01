
def _test_args_PIDController(obj):
    from sympy.physics.control.lti import PIDController
    if isinstance(obj, PIDController):
        kp, ki, kd, tf = obj.kp, obj.ki, obj.kd, obj.tf
        recreated_pid = PIDController(kp, ki, kd, tf, s)
        return recreated_pid == obj
    return False

