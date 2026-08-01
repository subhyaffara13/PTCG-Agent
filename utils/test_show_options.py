
def test_show_options():
    solver_methods = {
        'minimize': MINIMIZE_METHODS,
        'minimize_scalar': MINIMIZE_SCALAR_METHODS,
        'root': ROOT_METHODS,
        'root_scalar': ROOT_SCALAR_METHODS,
        'linprog': LINPROG_METHODS,
        'quadratic_assignment': QUADRATIC_ASSIGNMENT_METHODS,
    }
    for solver, methods in solver_methods.items():
        for method in methods:
            # testing that `show_options` works without error
            show_options(solver, method)

    unknown_solver_method = {
        'minimize': "ekki",  # unknown method
        'maximize': "cg",  # unknown solver
        'maximize_scalar': "ekki",  # unknown solver and method
    }
    for solver, method in unknown_solver_method.items():
        # testing that `show_options` raises ValueError
        assert_raises(ValueError, show_options, solver, method)

