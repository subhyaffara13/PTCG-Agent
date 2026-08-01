
def test_particular_case_1_with_adaptive_false():
    # Verify that symbolic expressions and numerical lambda functions are
    # evaluated with the same algorithm. In particular, uniform evaluation
    # is going to use np.vectorize, which correctly evaluates the following
    # mathematical function.
    if not np:
        skip("numpy not installed.")

    def do_test(a, b):
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

    s3 = LineOver1DRangeSeries(expr, (n, -10, 10), "",
        adaptive=False, n=10)
    s4 = LineOver1DRangeSeries(math_func, ("n", -10, 10), "",
        adaptive=False, n=10)
    do_test(s3, s4)

