
def test_slow_examples_1st_homogeneous_coeff_ode():
    _ode_solver_test(_get_examples_ode_sol_1st_homogeneous_coeff_subs_dep_div_indep, run_slow_test=True)
    _ode_solver_test(_get_examples_ode_sol_1st_homogeneous_coeff_best, run_slow_test=True)

