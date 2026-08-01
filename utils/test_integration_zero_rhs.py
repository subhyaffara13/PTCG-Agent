
def test_integration_zero_rhs(method, num_parallel_threads):
    if method == 'LSODA' and num_parallel_threads > 1:
        pytest.skip(reason='LSODA does not allow for concurrent execution')

    result = solve_ivp(fun_zero, [0, 10], np.ones(3), method=method)
    assert_(result.success)
    assert_equal(result.status, 0)
    assert_allclose(result.y, 1.0, rtol=1e-15)

