
def test_nth_linear_constant_coeff_undetermined_coefficients():
    #issue-https://github.com/sympy/sympy/issues/5787
    # This test case is to show the classification of imaginary constants under
    # nth_linear_constant_coeff_undetermined_coefficients
    eq = Eq(diff(f(x), x), I*f(x) + S.Half - I)
    our_hint = 'nth_linear_constant_coeff_undetermined_coefficients'
    assert our_hint in classify_ode(eq)
    _ode_solver_test(_get_examples_ode_sol_nth_linear_undetermined_coefficients)

