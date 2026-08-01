
def test_duplicate_timestamps():
    def upward_cannon(t, y):
        return [y[1], -9.80665]

    def hit_ground(t, y):
        return y[0]

    hit_ground.terminal = True
    hit_ground.direction = -1

    sol = solve_ivp(upward_cannon, [0, np.inf], [0, 0.01],
                    max_step=0.05 * 0.001 / 9.80665,
                    events=hit_ground, dense_output=True)
    assert_allclose(sol.sol(0.01), np.asarray([-0.00039033, -0.08806632]),
                    rtol=1e-5, atol=1e-8)
    assert_allclose(sol.t_events, np.asarray([[0.00203943]]), rtol=1e-5, atol=1e-8)
    assert_allclose(sol.y_events, [np.asarray([[ 0.0, -0.01 ]])], atol=1e-9)
    assert sol.success
    assert_equal(sol.status, 1)

