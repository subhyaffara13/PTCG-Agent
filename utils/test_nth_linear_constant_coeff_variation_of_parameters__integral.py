
def test_nth_linear_constant_coeff_variation_of_parameters__integral():
    # solve_variation_of_parameters shouldn't attempt to simplify the
    # Wronskian if simplify=False.  If wronskian() ever gets good enough
    # to simplify the result itself, this test might fail.
    our_hint = 'nth_linear_constant_coeff_variation_of_parameters_Integral'
    eq = f(x).diff(x, 5) + 2*f(x).diff(x, 3) + f(x).diff(x) - 2*x - exp(I*x)
    sol_simp = dsolve(eq, f(x), hint=our_hint, simplify=True)
    sol_nsimp = dsolve(eq, f(x), hint=our_hint, simplify=False)
    assert sol_simp != sol_nsimp
    assert checkodesol(eq, sol_simp, order=5, solve_for_func=False) == (True, 0)
    assert checkodesol(eq, sol_simp, order=5, solve_for_func=False) == (True, 0)

