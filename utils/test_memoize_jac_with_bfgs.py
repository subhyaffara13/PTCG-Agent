
def test_memoize_jac_with_bfgs(function_with_gradient):
    """ Tests that using MemoizedJac in combination with ScalarFunction
        and BFGS does not lead to repeated function evaluations.
        Tests changes made in response to GH11868.
    """
    memoized_function = MemoizeJac(function_with_gradient)
    jac = memoized_function.derivative
    hess = optimize.BFGS()

    x0 = np.array([1.0, 0.5])
    scalar_function = ScalarFunction(
        memoized_function, x0, (), jac, hess, None, None)
    assert function_with_gradient.number_of_calls.c == 1

    scalar_function.fun(x0 + 0.1)
    assert function_with_gradient.number_of_calls.c == 2

    scalar_function.fun(x0 + 0.2)
    assert function_with_gradient.number_of_calls.c == 3

