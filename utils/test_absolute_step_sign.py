
def test_absolute_step_sign():
    # test for gh12487
    # if an absolute step is specified for 2-point differences make sure that
    # the side corresponds to the step. i.e. if step is positive then forward
    # differences should be used, if step is negative then backwards
    # differences should be used.

    # function has double discontinuity at x = [-1, -1]
    # first component is \/, second component is /\
    def f(x):
        return -np.abs(x[0] + 1) + np.abs(x[1] + 1)

    # check that the forward difference is used
    grad = approx_derivative(f, [-1, -1], method='2-point', abs_step=1e-8)
    assert_allclose(grad, [-1.0, 1.0])

    # check that the backwards difference is used
    grad = approx_derivative(f, [-1, -1], method='2-point', abs_step=-1e-8)
    assert_allclose(grad, [1.0, -1.0])

    # check that the forwards difference is used with a step for both
    # parameters
    grad = approx_derivative(
        f, [-1, -1], method='2-point', abs_step=[1e-8, 1e-8]
    )
    assert_allclose(grad, [-1.0, 1.0])

    # check that we can mix forward/backwards steps.
    grad = approx_derivative(
        f, [-1, -1], method='2-point', abs_step=[1e-8, -1e-8]
     )
    assert_allclose(grad, [-1.0, -1.0])
    grad = approx_derivative(
        f, [-1, -1], method='2-point', abs_step=[-1e-8, 1e-8]
    )
    assert_allclose(grad, [1.0, 1.0])

    # the forward step should reverse to a backwards step if it runs into a
    # bound
    # This is kind of tested in TestAdjustSchemeToBounds, but only for a lower level
    # function.
    grad = approx_derivative(
        f, [-1, -1], method='2-point', abs_step=1e-8,
        bounds=(-np.inf, -1)
    )
    assert_allclose(grad, [1.0, -1.0])

    grad = approx_derivative(
        f, [-1, -1], method='2-point', abs_step=-1e-8, bounds=(-1, np.inf)
    )
    assert_allclose(grad, [-1.0, 1.0])

