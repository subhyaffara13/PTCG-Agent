
def test_nth_order_reducible():
    F = lambda eq: NthOrderReducible(SingleODEProblem(eq, f(x), x))._matches()
    D = Derivative
    assert F(D(y*f(x), x, y) + D(f(x), x)) == False
    assert F(D(y*f(y), y, y) + D(f(y), y)) == False
    assert F(f(x)*D(f(x), x) + D(f(x), x, 2))== False
    assert F(D(x*f(y), y, 2) + D(u*y*f(x), x, 3)) == False  # no simplification by design
    assert F(D(f(y), y, 2) + D(f(y), y, 3) + D(f(x), x, 4)) == False
    assert F(D(f(x), x, 2) + D(f(x), x, 3)) == True
    _ode_solver_test(_get_examples_ode_sol_nth_order_reducible)

