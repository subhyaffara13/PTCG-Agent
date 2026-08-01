
def test_function_calls(solver_name, rs_interface):
    # There do not appear to be checks that the bracketing solvers report the
    # correct number of function evaluations. Check that this is the case.
    solver = ((lambda f, a, b, **kwargs: root_scalar(f, bracket=(a, b)))
              if rs_interface else getattr(zeros, solver_name))

    def f(x):
        f.calls += 1
        return x**2 - 1
    f.calls = 0

    res = solver(f, 0, 10, full_output=True)

    if rs_interface:
        assert res.function_calls == f.calls
    else:
        assert res[1].function_calls == f.calls

