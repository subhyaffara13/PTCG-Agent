
def test_vode_jacobian_convention():
    # Regression test for gh-24933: VODE Jacobian transposition bug.
    def f(t, y):
        return [-0.04*y[0] + 1e4*y[1]*y[2],
                0.04*y[0] - 1e4*y[1]*y[2] - 3e7*y[1]**2,
                3e7*y[1]**2]

    def jac(t, y):
        return np.array([[-0.04,              1e4*y[2],         1e4*y[1]],
                         [0.04,  -1e4*y[2] - 6e7*y[1],        -1e4*y[1]],
                         [0.0,               6e7*y[1],              0.0]])

    y0 = [1.0, 0.0, 0.0]
    # Correct Jac. needs ~124 steps; transposed (bug) needs ~2084. Cap at 150.
    r = ode(f, jac).set_integrator('vode', method='bdf', rtol=1e-8,
                                   atol=1e-10, nsteps=150)
    r.set_initial_value(y0, 0.0)
    r.integrate(1.0)
    assert r.successful()

