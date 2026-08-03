import itertools

def test_banded_ode_solvers():
    # Test the "lsoda", "vode" and "zvode" solvers of the `ode` class
    # with a system that has a banded Jacobian matrix.

    # This test does not test the Jacobian evaluation (banded or not)
    # of "lsoda" due to the nonstiff nature of the equations.

    t_exact = np.linspace(0, 1.0, 5)

    # --- Real arrays for testing the "lsoda" and "vode" solvers ---

    # lband = 2, uband = 1:
    a_real = np.array([[-0.6, 0.1, 0.0, 0.0, 0.0],
                       [0.2, -0.5, 0.9, 0.0, 0.0],
                       [0.1, 0.1, -0.4, 0.1, 0.0],
                       [0.0, 0.3, -0.1, -0.9, -0.3],
                       [0.0, 0.0, 0.1, 0.1, -0.7]])

    # lband = 0, uband = 1:
    a_real_upper = np.triu(a_real)

    # lband = 2, uband = 0:
    a_real_lower = np.tril(a_real)

    # lband = 0, uband = 0:
    a_real_diag = np.triu(a_real_lower)

    real_matrices = [a_real, a_real_upper, a_real_lower, a_real_diag]
    real_solutions = []

    for a in real_matrices:
        y0 = np.arange(1, a.shape[0] + 1)
        y_exact = _analytical_solution(a, y0, t_exact)
        real_solutions.append((y0, t_exact, y_exact))

    def check_real(idx, solver, meth, use_jac, with_jac, banded):
        a = real_matrices[idx]
        y0, t_exact, y_exact = real_solutions[idx]
        t, y = _solve_linear_sys(a, y0,
                                 tend=t_exact[-1],
                                 dt=t_exact[1] - t_exact[0],
                                 solver=solver,
                                 method=meth,
                                 use_jac=use_jac,
                                 with_jacobian=with_jac,
                                 banded=banded)
        assert_allclose(t, t_exact)
        assert_allclose(y, y_exact)

    for idx in range(len(real_matrices)):
        p = [['vode', 'lsoda'],  # solver
             ['bdf', 'adams'],   # method
             [False, True],      # use_jac
             [False, True],      # with_jacobian
             [False, True]]      # banded
        for solver, meth, use_jac, with_jac, banded in itertools.product(*p):
            check_real(idx, solver, meth, use_jac, with_jac, banded)

    # --- Complex arrays for testing the "zvode" solver ---

    # complex, lband = 2, uband = 1:
    a_complex = a_real - 0.5j * a_real

    # complex, lband = 0, uband = 0:
    a_complex_diag = np.diag(np.diag(a_complex))

    complex_matrices = [a_complex, a_complex_diag]
    complex_solutions = []

    for a in complex_matrices:
        y0 = np.arange(1, a.shape[0] + 1) + 1j
        y_exact = _analytical_solution(a, y0, t_exact)
        complex_solutions.append((y0, t_exact, y_exact))

    def check_complex(idx, solver, meth, use_jac, with_jac, banded):
        a = complex_matrices[idx]
        y0, t_exact, y_exact = complex_solutions[idx]
        t, y = _solve_linear_sys(a, y0,
                                 tend=t_exact[-1],
                                 dt=t_exact[1] - t_exact[0],
                                 solver=solver,
                                 method=meth,
                                 use_jac=use_jac,
                                 with_jacobian=with_jac,
                                 banded=banded)
        assert_allclose(t, t_exact)
        assert_allclose(y, y_exact)

    for idx in range(len(complex_matrices)):
        p = [['bdf', 'adams'],   # method
             [False, True],      # use_jac
             [False, True],      # with_jacobian
             [False, True]]      # banded
        for meth, use_jac, with_jac, banded in itertools.product(*p):
            check_complex(idx, "zvode", meth, use_jac, with_jac, banded)

