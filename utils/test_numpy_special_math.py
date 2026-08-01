
def test_numpy_special_math():
    if not numpy:
        skip("numpy not installed")

    funcs = [expm1, log1p, exp2, log2, log10, hypot, logaddexp, logaddexp2]
    for func in funcs:
        if 2 in func.nargs:
            expr = func(x, y)
            args = (x, y)
            num_args = (0.3, 0.4)
        elif 1 in func.nargs:
            expr = func(x)
            args = (x,)
            num_args = (0.3,)
        else:
            raise NotImplementedError("Need to handle other than unary & binary functions in test")
        f = lambdify(args, expr)
        result = f(*num_args)
        reference = expr.subs(dict(zip(args, num_args))).evalf()
        assert numpy.allclose(result, float(reference))

    lae2 = lambdify((x, y), logaddexp2(log2(x), log2(y)))
    assert abs(2.0**lae2(1e-50, 2.5e-50) - 3.5e-50) < 1e-62  # from NumPy's docstring

