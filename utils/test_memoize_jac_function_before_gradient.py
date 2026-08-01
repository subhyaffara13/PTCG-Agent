
def test_memoize_jac_function_before_gradient(function_with_gradient):
    memoized_function = MemoizeJac(function_with_gradient)

    x0 = np.array([1.0, 2.0])
    assert_allclose(memoized_function(x0), 5.0)
    assert function_with_gradient.number_of_calls.c == 1

    assert_allclose(memoized_function.derivative(x0), 2 * x0)
    assert function_with_gradient.number_of_calls.c == 1, \
        "function is not recomputed " \
        "if gradient is requested after function value"

    assert_allclose(
        memoized_function(2 * x0), 20.0,
        err_msg="different input triggers new computation")
    assert function_with_gradient.number_of_calls.c == 2, \
        "different input triggers new computation"

