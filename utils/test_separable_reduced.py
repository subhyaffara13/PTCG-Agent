
def test_separable_reduced():
    df = f(x).diff(x)
    eq = (x / f(x))*df  + tan(x**2*f(x) / (x**2*f(x) - 1))
    assert classify_ode(eq) == ('factorable', 'separable_reduced', 'lie_group',
        'separable_reduced_Integral')
    _ode_solver_test(_get_examples_ode_sol_separable_reduced)

