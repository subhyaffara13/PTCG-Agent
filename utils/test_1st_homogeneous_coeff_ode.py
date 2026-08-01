
def test_1st_homogeneous_coeff_ode():
    #These were marked as test_1st_homogeneous_coeff_corner_case
    eq1 = f(x).diff(x) - f(x)/x
    c1 = classify_ode(eq1, f(x))
    eq2 = x*f(x).diff(x) - f(x)
    c2 = classify_ode(eq2, f(x))
    sdi = "1st_homogeneous_coeff_subs_dep_div_indep"
    sid = "1st_homogeneous_coeff_subs_indep_div_dep"
    assert sid not in c1 and sdi not in c1
    assert sid not in c2 and sdi not in c2
    _ode_solver_test(_get_examples_ode_sol_1st_homogeneous_coeff_subs_dep_div_indep)
    _ode_solver_test(_get_examples_ode_sol_1st_homogeneous_coeff_best)

