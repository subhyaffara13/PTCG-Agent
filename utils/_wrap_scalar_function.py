
def _wrap_scalar_function(function, args):
    # wraps a minimizer function to count number of evaluations
    # and to easily provide an args kwd.
    ncalls = [0]
    if function is None:
        return ncalls, None

    def function_wrapper(x, *wrapper_args):
        ncalls[0] += 1
        # A copy of x is sent to the user function (gh13740)
        fx = function(np.copy(x), *(wrapper_args + args))
        # Ideally, we'd like to a have a true scalar returned from f(x). For
        # backwards-compatibility, also allow np.array([1.3]), np.array([[1.3]]) etc.
        if not np.isscalar(fx):
            _dt = getattr(fx, "dtype", np.float64)
            try:
                fx = _dt.type(np.asarray(fx).item())
            except (TypeError, ValueError) as e:
                raise ValueError("The user-provided objective function "
                                 "must return a scalar value.") from e
        return fx

    return ncalls, function_wrapper

