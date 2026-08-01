
def test_particular_case_1_with_adaptive_true():
    # Verify that symbolic expressions and numerical lambda functions are
    # evaluated with the same algorithm.
    if not np:
        skip("numpy not installed.")

    # NOTE: xfail because sympy's adaptive algorithm is not deterministic

    def do_test(a, b):
        with warns(
            RuntimeWarning,
            match="invalid value encountered in scalar power",
            test_stacklevel=False,
        ):
            d1 = a.get_data()
            d2 = b.get_data()
            for t, v in zip(d1, d2):
                assert np.allclose(t, v)

    n = symbols("n")
    a = S(2) / 3
    epsilon = 0.01
    xn = (n**3 + n**2)**(S(1)/3) - (n**3 - n**2)**(S(1)/3)
    expr = Abs(xn - a) - epsilon
    math_func = lambdify([n], expr)
    s1 = LineOver1DRangeSeries(expr, (n, -10, 10), "",
        adaptive=True, depth=3)
    s2 = LineOver1DRangeSeries(math_func, ("n", -10, 10), "",
        adaptive=True, depth=3)
    do_test(s1, s2)

