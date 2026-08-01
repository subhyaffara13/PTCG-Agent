
def test_factorable():
    assert integrate(-asin(f(2*x)+pi), x) == -Integral(asin(pi + f(2*x)), x)
    _ode_solver_test(_get_examples_ode_sol_factorable)

