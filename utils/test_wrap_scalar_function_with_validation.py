
def test_wrap_scalar_function_with_validation():

    def func_(x):
        return x

    fcalls, func = optimize._optimize.\
        _wrap_scalar_function_maxfun_validation(func_, np.asarray(1), 5)

    for i in range(5):
        func(np.asarray(i))
        assert fcalls[0] == i+1

    msg = "Too many function calls"
    with assert_raises(optimize._optimize._MaxFuncCallError, match=msg):
        func(np.asarray(i))  # exceeded maximum function call

    fcalls, func = optimize._optimize.\
        _wrap_scalar_function_maxfun_validation(func_, np.asarray(1), 5)

    msg = "The user-provided objective function must return a scalar value."
    with assert_raises(ValueError, match=msg):
        func(np.array([1, 1]))

