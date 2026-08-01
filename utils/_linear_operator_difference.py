
def _linear_operator_difference(fun, x0, f0, h, method):
    m = f0.size
    n = x0.size

    result_dtype = xp_result_type(x0, f0, force_floating=True, xp=np)

    if method == '2-point':
        # nfev = 1
        def matvec(p):
            if np.array_equal(p, np.zeros_like(p)):
                return np.zeros(m, dtype=result_dtype)
            dx = h / norm(p)
            x = x0 + dx*p
            df = fun(x) - f0
            return df / dx

    elif method == '3-point':
        # nfev = 2
        def matvec(p):
            if np.array_equal(p, np.zeros_like(p)):
                return np.zeros(m, dtype=result_dtype)
            dx = 2*h / norm(p)
            x1 = x0 - (dx/2)*p
            x2 = x0 + (dx/2)*p
            f1 = fun(x1)
            f2 = fun(x2)
            df = f2 - f1
            return df / dx

    elif method == 'cs':
        # nfev = 1
        def matvec(p):
            if np.array_equal(p, np.zeros_like(p)):
                return np.zeros(m, dtype=result_dtype)
            dx = h / norm(p)
            x = x0 + dx*p*1.j
            f1 = fun(x)
            df = f1.imag
            return df / dx
    else:
        raise RuntimeError("Never be here.")

    return LinearOperator(shape=(m, n), matvec=matvec, dtype=result_dtype), 0

