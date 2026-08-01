
def test_issue_23348():
    steps = integral_steps(tan(x), x)
    constant_times_step = steps.substep.substep
    assert constant_times_step.integrand == constant_times_step.constant * constant_times_step.other

