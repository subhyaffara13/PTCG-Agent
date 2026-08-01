
def test_lambdify_derivative_and_functions_as_arguments():
    # see: https://github.com/sympy/sympy/issues/26663#issuecomment-2157179517
    t, a, b = symbols('t, a, b')
    f = Function('f')(t)
    args = f.diff(t, 2), f.diff(t), f, a, b
    expr1 = a*f.diff(t, 2) + b*f.diff(t) + a*b*f + a**2
    num_args = 2.0, 3.0, 4.0, 5.0, 6.0
    ref1 = 5*2 + 6*3 + 5*6*4 + 5**2

    expr2 = a*f.diff(t, 2) + b*f.diff(t) - a*b*f + b**2 - a**2
    ref2 = 5*2 + 6*3 - 5*6*4 + 6**2 - 5**2

    for dummify, _cse in product([False, None, True], [False, True]):
        func1 = lambdify(args, expr1, cse=_cse, dummify=dummify)
        res1 = func1(*num_args)
        assert abs(res1 - ref1) < 1e-12

        func12 = lambdify(args, [expr1, expr2], cse=_cse, dummify=dummify)
        res12 = func12(*num_args)
        assert len(res12) == 2
        assert abs(res12[0] - ref1) < 1e-12
        assert abs(res12[1] - ref2) < 1e-12

