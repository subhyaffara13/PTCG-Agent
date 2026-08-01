
def test_nth_algebraic():
    eqn = f(x) + f(x)*f(x).diff(x)
    solns = [Eq(f(x), exp(x)),
             Eq(f(x), C1*exp(C2*x))]
    solns_final =  _remove_redundant_solutions(eqn, solns, 2, x)
    assert solns_final == [Eq(f(x), C1*exp(C2*x))]

    _ode_solver_test(_get_examples_ode_sol_nth_algebraic)

