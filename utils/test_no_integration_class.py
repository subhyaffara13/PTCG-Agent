
def test_no_integration_class():
    for method in [RK23, RK45, DOP853, Radau, BDF, LSODA]:
        solver = method(lambda t, y: -y, 0.0, [10.0, 0.0], 0.0)
        solver.step()
        assert_equal(solver.status, 'finished')
        sol = solver.dense_output()
        assert_equal(sol(0.0), [10.0, 0.0])
        assert_equal(sol([0, 1, 2]), [[10, 10, 10], [0, 0, 0]])

        solver = method(lambda t, y: -y, 0.0, [], np.inf)
        solver.step()
        assert_equal(solver.status, 'finished')
        sol = solver.dense_output()
        assert_equal(sol(100.0), [])
        assert_equal(sol([0, 1, 2]), np.empty((0, 3)))

