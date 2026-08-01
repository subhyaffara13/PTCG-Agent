
def test_integration_stiff(method, num_parallel_threads):
    rtol = 1e-6
    atol = 1e-6
    y0 = [1e4, 0, 0]
    tspan = [0, 1e8]

    if method == 'LSODA' and num_parallel_threads > 1:
        pytest.skip(reason='LSODA does not allow for concurrent calls')

    def fun_robertson(t, state):
        x, y, z = state
        return [
            -0.04 * x + 1e4 * y * z,
            0.04 * x - 1e4 * y * z - 3e7 * y * y,
            3e7 * y * y,
        ]

    res = solve_ivp(fun_robertson, tspan, y0, rtol=rtol,
                    atol=atol, method=method)

    # If the stiff mode is not activated correctly, these numbers will be much bigger
    assert res.nfev < 5000
    assert res.njev < 200

